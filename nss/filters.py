import django_filters
from .models import volunteer  # Adjust import based on your actual model name

class VolunteerFilter(django_filters.FilterSet):
    class Meta:
        model = volunteer
        exclude = ['image','status','guard_name','guard_mob_no','dob','address','height','weight','mobile_no','Email_id','cultural_talents','hobbies','roll_no']
