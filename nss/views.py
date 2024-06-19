from django.shortcuts import render, get_object_or_404, redirect,reverse
from django.http import HttpResponse
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from .models import *
from django.contrib.auth.models import Group,User
from django.db import connection
from django.contrib.auth.decorators import login_required
from .decorators import group_required 
from .filters import VolunteerFilter

def access_denied(request):
    return render(request, 'nss/acess_denied.html')


@login_required()
def ns(request):
    #request.session.set_expiry(2)
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
@login_required()
def view_volunteer(request):
    volunteers = volunteer.objects.all()
    volunteer_filter = VolunteerFilter(request.GET, queryset=volunteers)
    filtered_volunteers = volunteer_filter.qs

    if volunteer_filter.form.is_bound and volunteer_filter.form.is_valid():
        # Filters are applied, display all filtered results without pagination
        volunteer_list = filtered_volunteers
    else:
        # No filters applied or form not valid, apply pagination
        paginator = Paginator(filtered_volunteers, 10)  # Show 10 volunteers per page
        page_number = request.GET.get('page')
        try:
            volunteer_list = paginator.page(page_number)
        except PageNotAnInteger:
            volunteer_list = paginator.page(1)
        except EmptyPage:
            volunteer_list = paginator.page(paginator.num_pages)

    context = {
        'volunteer_list': volunteer_list,
        'page_obj': volunteer_list,  # This is used by the template for pagination
        'myFilter': volunteer_filter,  # Pass the filter object to the context
    }
    return render(request, 'nss/view_volunteer.html', context)



@login_required()
def view_attendance2(request):
    vol={
        'vol':volunteer.objects.all()
    }
    return render(request,'nss/full_attendance.html',vol)
@login_required()
def view_attendance(request):
    eve = {
        'even': Event.objects.all().order_by('date').values()
    }
    if request.method == "POST":
        ev = request.POST.get('event')
        event_id=ev
        selected_event=Event.objects.get(event_id=ev)
        res = {
            'resul': Attendance.objects.filter(event=event_id).order_by('date').select_related('volunteer')
        }
        return render(request, 'nss/view_attendance.html',{**res,**eve,'selected_event': selected_event})
    return render(request,'nss/view_attendance.html',eve)
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

def edit_volunteer(request, pk):
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


@login_required()
def delete2(request, volunteer_name):
    vol={
        'voluntee':volunteer.objects.filter(volunteer_id=volunteer_name)
    }
    
    ev={
        'even':Attendance.objects.filter(volunteer=volunteer_name)
    }
    # Pass the volunteer details to the template
    return render(request, 'nss/delete_volunteer.html', {**vol,**ev})

@login_required()
def delete_volunteer(request, pk):
    Volunteer = get_object_or_404(volunteer, pk=pk)
    Volunteer.delete()
    return redirect('view_volunteer') 

@login_required()
def report_list(request):
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

@login_required()
def report_list_more(request,pk):
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

@login_required()
def view_event(request):
    event={
        'eve':Event.objects.all()
    }
    return render(request,'nss/view_event.html',event)

@login_required()
def edit_event(request,pk):

    return render(request,'nss/edit_event.html')

@login_required()
def delete_event(request,pk):
    event = get_object_or_404(Event, pk=pk)
    print(event)
    event.delete()
    return redirect('view_event')

@login_required()
def approve_attendance(request,pk):
    att=Attendance.objects.get(Attendance_id=pk)
    att.status="approved"
    att.save()
    return HttpResponse('submitted')

def add_attendance(request):
    eve = {
        'even': Event.objects.all().order_by('date').values()
    }
    return render(request, 'nss/add_attendance.html',eve)

def dep_wise(request):
    if request.method=="POST":
        unit=request.POST.get('unit')
        event=request.POST.get('event')
        event=Event.objects.get(event_id=event)
        dept={
            'pog':Programme.objects.all(),
            'unit':unit,
            'event':event,
            'vol':volunteer.objects.filter(unit=unit),
            'list':[1,2,3]
            }
        return render(request,'nss/unit_wise.html',dept)

@login_required()
def attendance(request,pk):
    if request.method == "POST":
        date = request.POST.get('date')
        id_list = request.POST.getlist('name')
        time=request.POST.get('time')
        for volunteer_id in id_list:
            volunteer_instance= volunteer.objects.get(volunteer_id=volunteer_id)

            # Save the attendance record
            event=Event.objects.get(event_id=pk)
            att = Attendance(volunteer=volunteer_instance,date=date,event=event,no_of_hours=time)
            att.save()

    return redirect('view_attendance')

def promote(request):
    objec=volunteer.objects.all()
    for i in objec:
        if i.year != 3:
            i.year+=1
        else:
            i.status='inactive'
        i.save()
    return HttpResponse('updated')

def more_attendance(request,pk):
    vol={
        'vol':volunteer.objects.filter(volunteer_id=pk)
    }
    return render(request,'nss/more_attendance.html',vol)