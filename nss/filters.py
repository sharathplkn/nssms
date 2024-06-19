import django_filters
from .models import volunteer  # Adjust import based on your actual model name

class VolunteerFilter(django_filters.FilterSet):
    class Meta:
        model = volunteer
        exclude=['image']
