from django.db import models

# Create your models here.
class Department(models.Model):
    dep_id=models.IntegerField(primary_key=True)
    dep_name=models.CharField(max_length=20,unique=True)
    def __str__(self):
        return f"{self.dep_name}"
class Programme(models.Model):
    programme_id=models.IntegerField(primary_key=True)
    dept=models.ForeignKey(Department,on_delete=models.CASCADE)
    program_name=models.CharField(max_length=65)
    no_of_sems=models.IntegerField()
    grad_level=models.CharField(max_length=10)
    def __str__(self):
        return f"{self.program_name}"
class volunteer(models.Model):
    volunteer_id=models.AutoField(primary_key=True)
    name=models.CharField(max_length=25)
    status=models.CharField(default='active',max_length=20)
    guard_name=models.CharField(max_length=25)
    guard_mob_no=models.IntegerField()
    sex=models.CharField(max_length=15)
    dob=models.DateField()
    year=models.IntegerField()
    community=models.CharField(max_length=15)
    address=models.TextField()
    blood_group=models.CharField(max_length=15)
    height=models.IntegerField()
    unit=models.IntegerField()
    weight=models.IntegerField()
    mobile_no=models.IntegerField()
    Email_id=models.EmailField()
    year_of_enrollment=models.IntegerField()    
    cultural_talents=models.TextField()
    hobbies=models.TextField()
    roll_no=models.IntegerField(unique=False,null=True)
    image=models.ImageField(upload_to='volunteers',default="")
    program=models.ForeignKey(Programme,on_delete=models.CASCADE)
    totalhours=models.IntegerField(null=True)
    def __str__(self):
        return f"{self.name}"

class Event(models.Model):
    event_id=models.AutoField(primary_key=True)
    event_name=models.CharField(max_length=60)
    date=models.DateField()
    def __str__(self):
        return f"{self.event_name}"
class Attendance(models.Model):
    Attendance_id=models.AutoField(primary_key=True)
    volunteer=models.ForeignKey(volunteer,on_delete=models.CASCADE,related_name='attendances')
    date=models.DateField()
    event=models.ForeignKey(Event,on_delete=models.CASCADE)
    status=models.CharField(max_length=40,default="Pending for Approval")
    no_of_hours=models.IntegerField()
    def __str__(self):
        return f"{self.event.event_name}"

class Event_details(models.Model):
    event=models.ForeignKey(Event,on_delete=models.CASCADE)
    start_time=models.TimeField(auto_now=False, auto_now_add=False)
    end_time=models.TimeField(auto_now=False, auto_now_add=False)
    des=models.TextField()
    def __str__(self):
        return f"{self.event.event_name}"

class Event_Photos(models.Model):
    event=models.ForeignKey(Event,on_delete=models.CASCADE)
    photo=models.ImageField(upload_to='events')