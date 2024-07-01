from django.shortcuts import render, get_object_or_404, redirect,reverse
from django.http import HttpResponse,HttpResponseBadRequest
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from .models import *
from django.contrib.auth.models import Group,User
from django.db import connection
from django.contrib.auth.decorators import login_required
from .decorators import group_required 
from datetime import datetime
from .filters import *
import os
from django.template.loader import get_template
from django.utils.timezone import now
from django.conf import settings

def access_denied(request):
    return render(request, 'nss/acess_denied.html')

@login_required()
def ns(request):
#request.session.set_expiry(2)
    events = Event.objects.filter(date__lte=now()).order_by('-date')[:5]
    volunteers = volunteer.objects.all()
    pending_approvals = Attendance_status.objects.filter(status="pending for approval")
    
    context = {
        'events': events,
        'volunteers': volunteers,
        'pending_approvals': pending_approvals
    }
    return render(request, 'nss/home.html', context)
@login_required()
def add_volunteer(request):
    try:
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
            Email_id=request.POST.get('email')
            year_of_enrollment=request.POST.get('year_of_enrollment')
            cultural_talents=request.POST.get('cultural_talents')
            hobbies=request.POST.get('hobbies')
            roll_no=request.POST.get('roll_no')
            image=request.FILES.get ('image')  
            unit=request.POST.get('unit') 
            programme_id=Programme.objects.get(program_name=programme_name)
            print(programme_id)
            voluntee=volunteer(unit=unit,image=image,name=name,guard_name=guard_name,guard_mob_no=guard_mob_no,sex=sex,dob=dob,program=programme_id,year=year,community=community,address=address,blood_group=blood_group,height=height,weight=weight,mobile_no=mobile_no,Email_id=Email_id,year_of_enrollment=year_of_enrollment,cultural_talents=cultural_talents,hobbies=hobbies,roll_no=roll_no)
            voluntee.save()

            return redirect('view_volunteer')
        return render(request,'nss/add_volunteer.html',prog)
    except Exception:
        return render(request,'nss/error.html')
@login_required()
def view_volunteer(request):
    try:
        volunteer_list = volunteer.objects.filter(status='active')
        volunteer_filter = VolunteerFilter(request.GET, queryset=volunteer_list)
        
        items_per_page = request.GET.get('items_per_page', 10)
        
        try:
            items_per_page = int(items_per_page)
        except ValueError:
            items_per_page = 10
        
        paginator = Paginator(volunteer_filter.qs, items_per_page)
        page_number = request.GET.get('page')
        page_obj = paginator.get_page(page_number)
        
        return render(request, 'nss/view_volunteer.html', {'filter': volunteer_filter, 'page_obj': page_obj, 'items_per_page': items_per_page})
    except Exception:
        return render(request,'nss/error.html')

@login_required()
def view_attendance2(request):
    try:
        volunteer_list = volunteer.objects.all()
        volunteer_filter = VolunteerFilter2(request.GET, queryset=volunteer_list)
        
        items_per_page = request.GET.get('items_per_page', 10)
        
        try:
            items_per_page = int(items_per_page)
        except ValueError:
            items_per_page = 10
        
        paginator = Paginator(volunteer_filter.qs, items_per_page)
        page_number = request.GET.get('page')
        page_obj = paginator.get_page(page_number)
        
        return render(request, 'nss/full_attendance.html', {'filter': volunteer_filter, 'page_obj': page_obj, 'items_per_page': items_per_page})
    except Exception:
        return render(request,'nss/error.html')
@login_required()
def view_attendance(request):
    eve = {
        'even': Attendance_status.objects.all().order_by('date').select_related('event')
    }
    
    if request.method == "POST":
        at_status_id = request.POST.get('event')
        return redirect('view_attendance3', status_id=at_status_id)
        
    return render(request, 'nss/view_attendance.html', eve)

@login_required()
def volunteer_details(request, volunteer_name):
    try:
        # Assuming you have a Volunteer model with a 'name' field
        vol={
            'voluntee':volunteer.objects.filter(volunteer_id=volunteer_name)
        }
        
        ev={
            'even':Attendance.objects.filter(volunteer=volunteer_name)
        }
        # Pass the volunteer details to the template
        return render(request, 'nss/volunteer_details.html', {**vol,**ev})
    except Exception:
        return render(request,'nss/error.html')
@login_required()
def event(request):
    try:

        return render(request,'nss/event.html')

    except Exception:
        return render(request,'nss/error.html')

@login_required()
def add_event(request):
    try:
        if request.method=="POST":
            event_name=request.POST.get('event_name')
            date=request.POST.get('date')
            ev=Event(event_name=event_name,date=date)
            ev.save()
            message="Submitted Successfully"
            return redirect(reverse('add_event') + '?message=' + message)
        return render(request,'nss/add_event.html')
    except Exception:
        return render(request,'nss/error.html')
@login_required()
def event_details(request):
    try:
        eve = {
            'even': Event.objects.all().order_by('date').values()
        }
        if request.method=="POST":
            event_id=request.POST.get('event_name')
            des=request.POST.get('des')
            event_id=Event.objects.get(event_id=event_id)
            event_exists = Event_details.objects.filter(event=event_id).exists()
            if not event_exists:
                ev=Event_details(event=event_id,des=des)
                ev.save()
                message="Submitted Successfully"
                return redirect(reverse('event_details') + '?message1=' + message)
            else:
                message="Already Exist"
                return redirect(reverse('event_details') + '?message2=' + message)
        return render(request,'nss/event_details.html',eve)
    except Exception:
        return render(request,'nss/error.html')
@login_required()
def report(request):
    try:
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
    except Exception:
        return render(request,'nss/error.html')
@login_required()
def event_photos(request):
    try:
        eve = {
            'even': Event.objects.all().order_by('date').values()
        }
        if request.method == "POST" and request.FILES:
            photo=request.FILES.get('photo')
            event=request.POST.get('event_name')
            event_id=Event.objects.get(event_name=event)
            if Event_Photos.objects.filter(event=event_id).count() >= 3:
                message = "Three images are already uploaded for this event."
                return redirect(reverse('event_photos') + '?message1=' + message)
            else:
                ev=Event_Photos(photo=photo,event=event_id)
                ev.save()
                message = "Uploaded Sucessfully"
                return redirect(reverse('event_photos') + '?message2=' + message)
        return render(request,'nss/add_photos.html',eve)
    except Exception:
        return render(request,'nss/error.html')
def event2(request):
    try:
        return render(request,'nss/event2.html')
    except Exception:
        return render(request,'nss/error.html')
def edit_volunteer(request, pk):
    try:
        Volunteer = get_object_or_404(volunteer, pk=pk)
        if request.method == "POST":
            name = request.POST.get('name')
            guard_name = request.POST.get('guard_name')
            guard_mob_no = request.POST.get('guard_mob_no')
            sex = request.POST.get('sex')
            dob = request.POST.get('dob')
            programme_name = request.POST.get('programme')
            year = request.POST.get('year')
            community = request.POST.get('community')
            address = request.POST.get('address')
            blood_group = request.POST.get('blood_group')
            height = request.POST.get('height')
            weight = request.POST.get('weight')
            unit = request.POST.get('unit')
            mobile_no = request.POST.get('mobile_no')
            Email_id = request.POST.get('email')
            year_of_enrollment = request.POST.get('year_of_enrollment')
            cultural_talents = request.POST.get('cultural_talents')
            hobbies = request.POST.get('hobbies')
            roll_no = request.POST.get('roll_no')
            if 'image' in request.FILES:
                image = request.FILES['image']
                Volunteer.image = image
            programme_id = Programme.objects.get(program_name=programme_name)

            Volunteer.name = name
            Volunteer.guard_name = guard_name
            Volunteer.guard_mob_no = guard_mob_no
            Volunteer.sex = sex
            Volunteer.dob = dob
            Volunteer.programme = programme_id
            Volunteer.year = year
            Volunteer.community = community
            Volunteer.address = address
            Volunteer.blood_group = blood_group
            Volunteer.height = height
            Volunteer.weight = weight
            Volunteer.mobile_no = mobile_no
            Volunteer.Email_id = Email_id
            Volunteer.year_of_enrollment = year_of_enrollment
            Volunteer.cultural_talents = cultural_talents
            Volunteer.hobbies = hobbies
            Volunteer.roll_no = roll_no
            Volunteer.unit=unit


            Volunteer.save()
            return redirect('view_volunteer')

        context = {
            'dep': Programme.objects.all(),
            'Volunteer': Volunteer
        }
        return render(request, 'nss/edit_volunteer.html', context)
    except Exception:
        return render(request,'nss/error.html')

@login_required()
def delete2(request, pk):
    try:
        vol={
            'voluntee':volunteer.objects.filter(volunteer_id=pk)
        }
        
        ev={
            'even':Attendance.objects.filter(volunteer=pk)
        }
        # Pass the volunteer details to the template
        return render(request, 'nss/delete_volunteer.html', {**vol,**ev})
    except Exception:
        return render(request,'nss/error.html')
@login_required()
def delete_volunteer(request, pk):
    try:
        Volunteer = get_object_or_404(volunteer, pk=pk)
        Volunteer.delete()
        return redirect('view_volunteer') 
    except Exception:
        return render(request,'nss/error.html')
@login_required()
def report_list(request):
    try:
        report={
            'event':Event.objects.all().order_by('date')
        }
        pics={
            'pics':Event_Photos.objects.all()
        }
        details={
            'details':Event_details.objects.all()
        }
        return render(request,'nss/report_list.html',{**report,**pics,**details})
    except Exception:
        return render(request,'nss/error.html')
@login_required()
def report_list_more(request,pk):
    try:
        event={
            'eve':Event.objects.filter(event_id=pk)
        }
        pics={
            'pics':Event_Photos.objects.filter(event_id=pk)
        }
        desc={
            'desc':Event_details.objects.filter(event_id=pk)
        }
        return render(request,'nss/report_list_more.html',{**event,**pics,**desc})
    except Exception:
        return render(request,'nss/error.html')
@login_required()
def view_event(request):
    try:
        event={
            'eve':Event.objects.all()
        }
        return render(request,'nss/view_event.html',event)
    except Exception:
        return render(request,'nss/error.html')

@login_required()
def delete_event(request,pk):
    try:
        event = get_object_or_404(Event, pk=pk)
        print(event)
        event.delete()
        return redirect('view_event')
    except Exception:
        return render(request,'nss/error.html')
@login_required()
def approve_attendance(request,pk):
    try:
        att=Attendance_status.objects.get(status_id=pk)
        att.status="approved"
        att.save()
        return redirect('view_attendance3', status_id=pk) 
    except Exception:
        return render(request,'nss/error.html')
@login_required()
def reject_attendance(request,pk):
    try:
        att=Attendance_status.objects.get(status_id=pk)
        att.status="rejected"
        att.save()
        return redirect('view_attendance3', status_id=pk) 
    except Exception:
        return render(request,'nss/error.html')
def add_attendance(request):
    try:
        eve = {
            'even': Event.objects.all().order_by('date').values()
        }
        return render(request, 'nss/add_attendance.html',eve)
    except Exception:
        return render(request,'nss/error.html')
def dep_wise(request):
    try:
        if request.method=="POST":
            unit=request.POST.get('unit')
            event=request.POST.get('event')
            event=Event.objects.get(event_id=event)
            dept={
                'pog':Programme.objects.all(),
                'unit':unit,
                'event':event,
                'vol':volunteer.objects.filter(unit=unit,status='active'),
                'list':[1,2,3]
                }
            return render(request,'nss/unit_wise.html',dept)
    except Exception:
        return render(request,'nss/error.html')
@login_required()
def attendance(request,pk,unit):
    try:
        if request.method == "POST":
            date = request.POST.get('date')
            event=Event.objects.get(event_id=pk)

            event = get_object_or_404(Event, event_id=pk)
            
            # Check if attendance for this event on the given date already exists
            existing_attendance = Attendance_status.objects.filter(event=event, date=date,unit=unit).exists()
            
            if existing_attendance:
                message="Attendance for this event on the specified date already exists."
                return redirect(reverse('attendance') +'?message=' + message)
            
            id_list = request.POST.getlist('name')
            time=request.POST.get('time')
            at_status=Attendance_status(event=event,date=date,unit=unit)
            at_status.save()
            for volunteer_id in id_list:
                volunteer_instance= volunteer.objects.get(volunteer_id=volunteer_id)

                # Save the attendance record
                event=Event.objects.get(event_id=pk)
                att = Attendance(Attendance_status=at_status,volunteer=volunteer_instance,date=date,event=event,no_of_hours=time)
                att.save()

        return redirect('view_attendance')
    except Exception:
        return render(request,'nss/error.html')

@group_required('po')
def promote(request):
    try:
        objec=volunteer.objects.all()
        for i in objec:
            if i.year != 3:
                i.year+=1
            else:
                i.status='inactive'
            i.save()
        message="Promoted"
        return redirect(reverse('promote_check') +'?message=' + message)
    except Exception:
        return render(request,'nss/error.html')

def more_attendance(request,pk):
    try:
        vol={
            'vol':volunteer.objects.filter(volunteer_id=pk)
        }
        return render(request,'nss/more_attendance.html',vol)
    except Exception:
        return render(request,'nss/error.html')

@login_required()
def delete_attendance(request,pk):
    try:
        att=get_object_or_404(Attendance_status,status_id=pk)
        att.delete()
        return redirect('view_attendance')
    except Exception:
        return render(request,'nss/error.html')
@login_required()
def delete_images(request,pk,ev):
    try:
        pic=get_object_or_404(Event_Photos,id=pk)
        pic.delete()
        photo_path = os.path.join(settings.MEDIA_ROOT, str(pic.photo))
        if os.path.exists(photo_path):
            os.remove(photo_path) 
        message = "Deleted Successfully."
        return redirect(reverse('edit_event', args=[ev])+ '?message=' + message) 
    except Exception:
        return render(request,'nss/error.html')
@login_required()
def edit_event(request,pk):
    eve={
        'eve':Event.objects.filter(event_id=pk)
    }
    ev=Event.objects.get(event_id=pk)
    event_Photos = Event_Photos.objects.get(event=ev)
    event_details = Event_details.objects.get(event=ev)
    event1 = get_object_or_404(Event, pk=pk)
    if request.method=='POST':
        event_name=request.POST.get('event_name')
        date=request.POST.get('date')
        des=request.POST.get('des')
        event_details.des=des
        event1.event_name=event_name
        event1.date=date
        if event_details.des:
            event_details.save()
        event1.save()
        return redirect('view_event')
    return render(request,'nss/edit_event.html',eve)
@login_required()
def promote_check(request):
    try:
        return render(request,'nss/promote.html')
    except Exception:
        return render(request,'nss/error.html')

@login_required()
def monthly_report(request):
    try:
        if request.method=="POST":
            year=request.POST.get('year')
            print(year)
            month=request.POST.get('month')
            print(month)
            events = Event.objects.filter(date__year=year, date__month=month)
            details = Event_details.objects.filter(event__in=events)
            pics = Event_Photos.objects.filter(event__in=events)
            return render(request, 'nss/report.html', {'event': events, 'details': details, 'pics': pics})
    except Exception:
        return render(request,'nss/error.html')
@login_required()
def yearly_report(request):
    try:
        if request.method=='POST':
            year=request.POST.get('year')
            print(f"Year received: {year}")  # Add a debug print statement
            print(f"Year received: {year}, type: {type(year)}")
            events = Event.objects.filter(date__year=year)
            print(events)  # Add a debug print statement
            details = Event_details.objects.filter(event__in=events)
            pics = Event_Photos.objects.filter(event__in=events)
            return render(request, 'nss/report.html', {'event': events, 'details': details, 'pics': pics})
    except Exception:
        return render(request,'nss/error.html')
@login_required()
def select_month(request):
    try:
        return render(request,'nss/select_month.html')
    except Exception:
        return render(request,'nss/error.html')
@login_required()
def select_year(request):
    try:
        return render(request,'nss/select_year.html')
    except Exception:
        return render(request,'nss/error.html')


@login_required()
def view_attendance3(request,status_id):
    at_status=Attendance_status.objects.get(status_id=status_id)
    res = {
        'resul': Attendance.objects.filter(Attendance_status=at_status).order_by('date').select_related('volunteer')
    }
    status={
        'status':Attendance_status.objects.get(status_id=status_id)
    }
    return render(request, 'nss/view_attendance3.html',{**status,**res,'status_id': status_id})
