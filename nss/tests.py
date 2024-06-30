from django.test import TestCase
from django.utils import timezone
from .models import Department, Programme, volunteer, Event, Attendance_status, Attendance, Event_details, Event_Photos
from django.contrib.auth.models import User, Group

class ProgrammeModelTest(TestCase):

    def setUp(self):
        self.department = Department.objects.create(dep_id=1, dep_name="Computer Science")
        self.programme = Programme.objects.create(
            programme_id=1,
            dept=self.department,
            program_name="BSc Computer Science",
            no_of_sems=6,  # Make sure to provide a value for no_of_sems
            grad_level="Undergraduate"
        )

    def test_programme_creation(self):
        self.assertEqual(self.programme.program_name, "BSc Computer Science")
        self.assertEqual(self.programme.no_of_sems, 6)
        self.assertEqual(str(self.programme), "BSc Computer Science")
