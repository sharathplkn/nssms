#myapp/management/commands/populate_volunteers.py

from django.core.management.base import BaseCommand
from nss.models import volunteer, Programme  # Adjust according to your app name
from faker import Faker
import random
from datetime import date, timedelta

class Command(BaseCommand):
    help = 'Populate volunteer model with random data'

    def handle(self, *args, **kwargs):
        faker = Faker()

        # Assuming you have some Programme objects in the database
        programmes = list(Programme.objects.all())
        if not programmes:
            self.stdout.write(self.style.ERROR('No Programme objects found. Please create some Programme objects first.'))
            return

        for _ in range(100):  # Adjust the range as needed
            name = faker.name()
            guard_name = faker.name()
            guard_mob_no = faker.random_number(digits=10)
            sex = random.choice(['Male', 'Female', 'Other'])
            dob = faker.date_of_birth(minimum_age=18, maximum_age=60)
            year = random.randint(1, 3)
            community = random.choice(['General', 'ST', 'SC','OBC'])
            address = faker.address()
            blood_group = random.choice(['A+', 'A-', 'B+', 'B-', 'AB+', 'AB-', 'O+', 'O-'])
            height = random.randint(150, 200)
            unit = random.randint(1, 3)
            weight = random.randint(50, 100)
            mobile_no = faker.random_number(digits=10)
            email_id = faker.email()
            year_of_enrollment = random.randint(2000, 2023)
            cultural_talents = faker.text(max_nb_chars=200)
            hobbies = faker.text(max_nb_chars=200)
            roll_no = faker.random_number(digits=5)
            image = faker.file_name(category='image')
            program = random.choice(programmes)

            volunteer.objects.create(
                name=name,
                guard_name=guard_name,
                guard_mob_no=guard_mob_no,
                sex=sex,
                dob=dob,
                year=year,
                community=community,
                address=address,
                blood_group=blood_group,
                height=height,
                unit=unit,
                weight=weight,
                mobile_no=mobile_no,
                Email_id=email_id,
                year_of_enrollment=year_of_enrollment,
                cultural_talents=cultural_talents,
                hobbies=hobbies,
                roll_no=roll_no,
                image=image,
                program=program
            )

        self.stdout.write(self.style.SUCCESS('Successfully populated volunteer model with random data'))
