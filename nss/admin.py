"""
from django.contrib import admin
from .models import *
# Register your models here.

admin.site.register(volunteer)
admin.site.register(Department)
admin.site.register(Attendance)
admin.site.register(Event)
admin.site.register(Programme)
admin.site.register(Event_details)
admin.site.register(Event_Photos)
admin.site.register(Attendance_status)
admin.site.register(Camp)
admin.site.register(Camp_Attendance)
admin.site.register(Camp_event)
admin.site.register(Camp_event_photos)"""


from django.contrib import admin
from .models import (
    volunteer, Department, Attendance, Event, Programme, Event_details,
    Event_Photos, Attendance_status, Camp, Camp_Attendance, Camp_event, Camp_event_photos
)

@admin.register(Department)
class DepartmentAdmin(admin.ModelAdmin):
    search_fields = ['dep_name']
    list_filter = ['dep_name']

@admin.register(Programme)
class ProgrammeAdmin(admin.ModelAdmin):
    search_fields = ['program_name', 'grad_level']
    list_filter = ['grad_level', 'no_of_sems', 'dept']

@admin.register(volunteer)
class VolunteerAdmin(admin.ModelAdmin):
    search_fields = ['name', 'Email_id', 'mobile_no']
    list_filter = ['status', 'year', 'community', 'blood_group', 'unit', 'program']

@admin.register(Event)
class EventAdmin(admin.ModelAdmin):
    search_fields = ['event_name']
    list_filter = ['date']

@admin.register(Attendance_status)
class AttendanceStatusAdmin(admin.ModelAdmin):
    search_fields = ['event__event_name', 'status']
    list_filter = ['date', 'unit', 'status']

@admin.register(Attendance)
class AttendanceAdmin(admin.ModelAdmin):
    search_fields = ['volunteer__name', 'event__event_name']
    list_filter = ['date', 'event']

@admin.register(Event_details)
class EventDetailsAdmin(admin.ModelAdmin):
    search_fields = ['event__event_name']
    list_filter = ['event']

@admin.register(Event_Photos)
class EventPhotosAdmin(admin.ModelAdmin):
    search_fields = ['event__event_name']
    list_filter = ['event']

@admin.register(Camp)
class CampAdmin(admin.ModelAdmin):
    search_fields = ['camp_name']
    list_filter = ['fromdate', 'todate']

@admin.register(Camp_Attendance)
class CampAttendanceAdmin(admin.ModelAdmin):
    search_fields = ['volunteer__name', 'camp__camp_name']
    list_filter = ['camp']

@admin.register(Camp_event)
class CampEventAdmin(admin.ModelAdmin):
    search_fields = ['event_name', 'camp__camp_name']
    list_filter = ['date', 'camp']

@admin.register(Camp_event_photos)
class CampEventPhotosAdmin(admin.ModelAdmin):
    search_fields = ['event__event_name']
    list_filter = ['event']
