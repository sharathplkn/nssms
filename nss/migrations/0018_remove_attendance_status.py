# Generated by Django 5.0.6 on 2024-06-22 13:31

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ("nss", "0017_rename_event_attendance_status_event"),
    ]

    operations = [
        migrations.RemoveField(
            model_name="attendance",
            name="status",
        ),
    ]
