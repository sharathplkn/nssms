from django.shortcuts import render
from django.http import HttpResponse
from .models import *
from django.db import connection
from django.contrib.auth.decorators import login_required

# Create your views here.
@login_required()
def ns(request):
    return render(request,'nss/home.html')
@login_required()
def add_volunteer(request):
    prog={
        'dep':Programme.objects.all()
    }
    if request.method=="POST" and request.FILES:
        name=request.POST.get('name')
        guard_name=request.POST.get('guard_name')
        guard_mob_no=request.POST.get('guard_mob_no')
        sex=request.POST.get('sex')
        dob=request.POST.get('dob')
        programme_name=request.POST.get('programme')
        year=request.POST.get('year')
        community=request.POST.get('community')
        address=request.POST.get('address')
        blood_group=request.POST.get('blood_group')
        height=request.POST.get('height')
        weight=request.POST.get('weight')
        mobile_no=request.POST.get('mobile_no')
        Email_id=request.POST.get('Email_id')
        year_of_enrollment=request.POST.get('year_of_enrollment')
        cultural_talents=request.POST.get('cultural_talents')
        hobbies=request.POST.get('hobbies')
        roll_no=request.POST.get('roll_no')
        image=request.FILES.get ('image')   
        programme_id=Programme.objects.get(program_name=programme_name)
        print(programme_id)
        voluntee=volunteer(image=image,name=name,guard_name=guard_name,guard_mob_no=guard_mob_no,sex=sex,dob=dob,program=programme_id,year=year,community=community,address=address,blood_group=blood_group,height=height,weight=weight,mobile_no=mobile_no,Email_id=Email_id,year_of_enrollment=year_of_enrollment,cultural_talents=cultural_talents,hobbies=hobbies,roll_no=roll_no)
        voluntee.save()

        return HttpResponse('submitted')
    return render(request,'nss/form.html',prog)
@login_required()
def view_volunteer(request):
    vol={
        'volunteer':volunteer.objects.all()
    }
    return render(request,'nss/view_volunteer.html',vol)
@login_required()
def attendance(request):
    vole = {
        'vol': volunteer.objects.all()
    }
    eve = {
        'even': Event.objects.all().order_by('date').values()
    }

    if request.method == "POST":
        datet = request.POST.get('date')
        name_list = request.POST.getlist('name')
        event=request.POST.get('event')
        time=request.POST.get('time')
        #converting roll_numbers from string to Integers

        for name_department in name_list:
            # Split the value into roll_no and department_name
            name, department_name = name_department.split('_')

            # Convert roll_no to an integer
            volunteer_instance= volunteer.objects.get(name=name)
            # Save the attendance record
            event=Event.objects.get(event_name=event)
            att = Attendance(volunteer=volunteer_instance,date=datet, name=name, department=department_name,event=event)
            att.save()

        return HttpResponse("Attendance Submitted")

    return render(request, 'nss/attendance.html',{**vole,**eve})
@login_required()
def view_attendance(request):
    at={
        'atte':Attendance.objects.all().order_by('date','department').values()
    }
    return render(request,'nss/view_attendance.html',at)
@login_required()
def view_attendance2(request):
    eve = {
        'even': Event.objects.all().order_by('date').values()
    }
    if request.method == "POST":
        ev = request.POST.get('event')
        selected_event=ev
        event_id=Event.objects.get(event_name=ev).event_id
        res = {
            'resul': Attendance.objects.filter(event=event_id).order_by('date').values()
        }
        return render(request, 'nss/sample.html',{**res,**eve,'selected_event': selected_event})
    return render(request,'nss/sample.html',eve)
@login_required()
def volunteer_details(request, volunteer_name):
    # Assuming you have a Volunteer model with a 'name' field
    vol={
        'voluntee':volunteer.objects.filter(volunteer_id=volunteer_name)
    }
    
    ev={
        'even':Attendance.objects.filter(volunteer=volunteer_name)
    }
    # Pass the volunteer details to the template
    return render(request, 'nss/volunteer_details.html', {**vol,**ev})

@login_required()
def event(request):

    return render(request,'nss/event.html')



@login_required()
def add_event(request):
    if request.method=="POST":
        event_name=request.POST.get('event_name')
        date=request.POST.get('date')
        ev=Event(event_name=event_name,date=date)
        ev.save()
        return HttpResponse('submitted')
    return render(request,'nss/add_event.html')

@login_required()
def event_details(request):
    eve = {
        'even': Event.objects.all().order_by('date').values()
    }
    if request.method=="POST":
        event=request.POST.get('event_name')
        start_time=request.POST.get('start_time')
        end_time=request.POST.get('end_time')
        des=request.POST.get('des')
        event_id=Event.objects.get(event_name=event)
        event_exists = Event_details.objects.filter(event=event_id).exists()
        if not event_exists:
            ev=Event_details(event=event_id,start_time=start_time,end_time=end_time,des=des)
            ev.save()
            return HttpResponse('submitted')
        else:
            return HttpResponse('Already Exist')
    return render(request,'nss/event_details.html',eve)

@login_required()
def report(request):
    report={
        'event':Event.objects.all()
    }
    pics={
        'pics':Event_Photos.objects.all()
    }
    details={
        'details':Event_details.objects.all()
    }
    return render(request,'nss/report.html',{**report,**pics,**details})

@login_required()
def event_photos(request):
    eve = {
        'even': Event.objects.all().order_by('date').values()
    }
    if request.method == "POST" and request.FILES:
        photo=request.FILES.get('photo')
        event=request.POST.get('event_name')
        event_id=Event.objects.get(event_name=event)
        ev=Event_Photos(photo=photo,event=event_id)
        ev.save()
        return HttpResponse('submitted')
    return render(request,'nss/add_photos.html',eve)
def event2(request):

    return render(request,'nss/event2.html')