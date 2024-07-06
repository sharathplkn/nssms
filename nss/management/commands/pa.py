from django.core.management.base import BaseCommand
import pandas as pd
import requests
from PIL import Image
from io import BytesIO
from django.core.files.base import ContentFile
from nss.models import volunteer, Programme
from django.core.exceptions import ObjectDoesNotExist
from django.core.files import File
from django.conf import settings
import os
import logging

logger = logging.getLogger(__name__)

class Command(BaseCommand):
    help = 'Import volunteers from an Excel file'

    def download_image_from_google_drive(self, link):
        try:
            if 'drive.google.com' in link:
                if '/d/' in link:
                    file_id = link.split('/d/')[1].split('/')[0]
                elif 'id=' in link:
                    file_id = link.split('id=')[1]
                else:
                    logger.error(f"Invalid Google Drive link format: {link}")
                    return None
            else:
                logger.error(f"Invalid Google Drive link: {link}")
                return None

            url = f"https://drive.google.com/uc?export=download&id={file_id}"

            response = requests.get(url)
            logger.info(f"Response status code: {response.status_code}")
            logger.info(f"Response content type: {response.headers.get('Content-Type')}")

            if response.status_code == 200:
                try:
                    image = Image.open(BytesIO(response.content))
                    image.verify()  # Verify that the image data is not corrupted
                    return image
                except Exception as e:
                    logger.error(f"Error opening image: {e}")
                    return None
            else:
                logger.error(f"Failed to download image from: {url}")
                return None
        except Exception as e:
            logger.error(f"Error downloading image from Google Drive: {e}")
            return None

    def handle(self, *args, **kwargs):
        excel_file_path = '/home/sharath/Downloads/Copy of NSS (Responses).xlsx'  # Adjust the path to your Excel file
        data = pd.read_excel(excel_file_path)

        required_columns = [
            'name', 'guard_name', 'guard_mob_no', 'sex', 'dob', 'image', 
            'program', 'year', 'community', 'address', 'blood_group', 
            'unit', 'weight', 'height', 'mobile_no', 'Email_id', 
            'year_of_enrollment', 'roll_no', 'cultural_talents', 'hobbies'
        ]

        missing_columns = [col for col in required_columns if col not in data.columns]
        if missing_columns:
            logger.error(f"Missing columns in the Excel file: {missing_columns}")
            return

        for index, row in data.iterrows():
            try:
                program, created = Programme.objects.get_or_create(program_name=row['program'])

                image = self.download_image_from_google_drive(row['image'])

                if image:
                    image_content = ContentFile(image.tobytes())
                else:
                    image_content = None

                weight_value = row['weight'] if 'weight' in data.columns and pd.notnull(row['weight']) else None

                volunteer_instance = volunteer.objects.create(
                    name=row['name'],
                    guard_name=row['guard_name'],
                    guard_mob_no=row['guard_mob_no'],
                    sex=row['sex'],
                    dob=pd.to_datetime(row['dob']).date(),
                    year=row['year'],
                    community=row['community'],
                    address=row['address'],
                    blood_group=row['blood_group'],
                    height=row['height'],
                    unit=row['unit'],
                    weight=weight_value,
                    mobile_no=row['mobile_no'],
                    Email_id=row['Email_id'] if 'Email_id' in data.columns else None,
                    year_of_enrollment=row['year_of_enrollment'],
                    cultural_talents=row['cultural_talents'],
                    hobbies=row['hobbies'],
                    roll_no=row['roll_no'],
                    image=image_content,
                    program=program
                )

                if image_content:
                    image_content.close()

            except ObjectDoesNotExist as e:
                logger.error(f"Programme does not exist: {e}")
            except Exception as e:
                logger.error(f"Error creating volunteer: {e}")

        self.stdout.write(self.style.SUCCESS('Data has been successfully imported.'))
