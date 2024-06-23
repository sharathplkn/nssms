from django.urls import path
from . import views

urlpatterns=[
    path('access-denied/', views.access_denied, name='access_denied'),
    path('',views.ns,name='ns'),
    path('nss',views.add_volunteer,name='add_volunteer'),
    path('event',views.event,name='event'),
    path('event_details',views.event_details,name='event_details'),
    path("vol",views.view_volunteer,name='view_volunteer'),
    path('add_attendance/<int:pk>/<int:unit>/',views.attendance,name='attendance'),
    path('att2',views.view_attendance2,name='view_attendance2'),
    path('att',views.view_attendance,name='view_attendance'),
    path('volunteer2/<str:volunteer_name>/',views.volunteer_details, name='volunteer_details'),
    path('even',views.add_event,name='add_event'),
    path('report',views.report,name='report'),
    path('event_photos',views.event_photos,name='event_photos'),
    path('event2',views.event2,name='event2'),
    path('volunteer/<int:pk>/edit/',views.edit_volunteer, name='edit_volunteer'),
    path('volunteer/<str:volunteer_name>/',views.delete2,name='delete2'),
    path('volunteer/<int:pk>/delete/', views.delete_volunteer, name='delete_volunteer'),
    path('report_list',views.report_list,name='report_list'),
    path('report_list_more/<int:pk>/',views.report_list_more,name='report_list_more'),
    path('view_event',views.view_event,name='view_event'),
    path('edit_event/<int:pk>/',views.edit_event,name='edit_event'),
    path('delete_event/<int:pk>/',views.edit_event,name='delete_event'),
    path('approve_attendance/<int:pk>',views.approve_attendance,name='approve_attendance'),
    path('att3',views.add_attendance,name='att3'),
    path('unit_wise',views.dep_wise,name='unit_wise'),
    path('promote',views.promote,name='promote'),
    path('more_attendance<int:pk>/',views.more_attendance,name='more_attendance')
]