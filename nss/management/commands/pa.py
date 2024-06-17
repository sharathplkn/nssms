# myapp/management/commands/populate_attendance.py

from django.core.management.base import BaseCommand
from nss.models import Attendance, volunteer, Event  # Adjust according to your app name
from faker import Faker
import random

class Command(BaseCommand):
    help = 'Populate Attendance model with random data'

    def handle(self, *args, **kwargs):
        faker = Faker()

        # Assuming you have some volunteer and Event objects in the database
        volunteers = list(volunteer.objects.all())
        events = list(Event.objects.all())
        
        if not volunteers:
            self.stdout.write(self.style.ERROR('No volunteer objects found. Please create some volunteer objects first.'))
            return
        
        if not events:
            self.stdout.write(self.style.ERROR('No Event objects found. Please create some Event objects first.'))
            return

        for _ in range(10000):  # Adjust the range as needed
            volunteer_obj = random.choice(volunteers)
            event_obj = random.choice(events)
            date = faker.date_this_year()
            status = random.choice(['Pending for Approval'])
            no_of_hours = random.randint(1, 5)

            Attendance.objects.create(
                volunteer=volunteer_obj,
                date=date,
                event=event_obj,
                status=status,
                no_of_hours=no_of_hours
            )

        self.stdout.write(self.style.SUCCESS('Successfully populated Attendance model with random data'))
