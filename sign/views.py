from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect
from django.contrib import auth
from django.contrib.auth.decorators import login_required
from sign.models import Event, Guest
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.shortcuts import render, get_object_or_404
from sign.forms import AddEventForm, AddGuestForm

# Create your views here.
def index(request):
    return render(request, "index.html")

def login_action(request):
    if request.method == 'POST':
        username = request.POST.get('username','')
        password = request.POST.get('password','')
        user = auth.authenticate(username=username, password=password)
        if user is not None:
            auth.login(request, user)
            response = HttpResponseRedirect('/event_manage/')
            #add browser cookie
            #response.set_cookie('user', username, 3600)
            #add session record to browser
            request.session['user'] = username
            return response
        else:
            return render(request, 'index.html', {'error': 'username or password error!'})

@login_required
def event_manage(request):
    # get browser cookie
    #username = request.COOKIES.get('usr','')
    #get browser session
    #username = request.session.get('user','')
    event_list = Event.objects.all()
    username = request.session.get('user', '')
    return render(request,"event_manage.html", {"user": username,
                                                "events": event_list})

@login_required
def add_event(request):
    username = request.session.get('user', '')

    if request.method == 'POST':
        form = AddEventForm(request.POST) # form 包含提交的数据
        if form.is_valid():
            name = form.cleaned_data['name']
            address = form.cleaned_data['address']
            limit = form.cleaned_data['limit']
            start_time = form.cleaned_data['start_time']
            status = form.cleaned_data['status']
            if status is True:
                status = 1
            else:
                status = 0

            Event.objects.create(name=name,limit=limit,address=address,status=status,start_time=start_time)
            return render(request, "add_event.html", {"user": username, "form": form, "success": "添加发布会成功!"})

    else:
        form = AddEventForm()

    return render(request, "add_event.html", {"user": username, "form": form})

@login_required
def search_name(request):
    username = request.session.get('user', '')
    search_name = request.GET.get("name", "")
    event_list = Event.objects.filter(name__contains=search_name)
    if len(event_list) == 0:
        return render(request, "event_manage.html", {"user": username,
                                                     "hint": "Query result is empty base on the event name!"})
    return render(request, "event_manage.html", {"user": username,
                                                 "events": event_list})

@login_required
def guest_manage(request):
    username = request.session.get('user', '')
    guest_list = Guest.objects.all()
    paginator = Paginator(guest_list, 2)
    page = request.GET.get('page')
    try:
        contacts = paginator.page(page)
    except PageNotAnInteger:
        #If page is not Integer, get first page
        contacts = paginator.page(1)
    except EmptyPage:
        #If page is not in the range, get last page
        contacts = paginator.page(paginator.num_pages)
    return render(request, "guest_manage.html", {"user": username,
                                                 "guests": contacts})
@login_required
def add_guest(request):
    username = request.session.get('user', '')

    if request.method == 'POST':
        form = AddGuestForm(request.POST)

        if form.is_valid():
            event = form.cleaned_data['event']
            realname = form.cleaned_data['realname']
            phone = form.cleaned_data['phone']
            email = form.cleaned_data['email']
            sign = form.cleaned_data['sign']
            if sign is True:
                sign = 1
            else:
                sign = 0

            Guest.objects.create(event=event,realname=realname,phone=phone,email=email,sign=sign)
            return render(request, "add_guest.html", {"user": username, "form": form, "success": "添加嘉宾成功!"})

    else:
        form = AddGuestForm()

    return render(request, "add_guest.html", {"user": username, "form": form})

@login_required
def search_phone(request):
    username = request.session.get('user', '')
    search_phone = request.GET.get("phone", "")
    guests = Guest.objects.filter(phone__contains=search_phone)
    if len(guests) == 0:
        return render(request, "guest_manage.html", {"user": username,
                                                     "hint": "Query result is empty base on phone"})

    paginator = Paginator(guests, 2)  #少于2条数据不够分页会产生警告
    page = request.GET.get('page')
    try:
        contacts = paginator.page(page)
    except PageNotAnInteger:
        # If page is not an integer, deliver first page.
        contacts = paginator.page(1)
    except EmptyPage:
        # If page is out of range (e.g. 9999), deliver last page of results.
        contacts = paginator.page(paginator.num_pages)
    return render(request, "guest_manage.html", {"user": username,
                                                 "guests": contacts,
                                                 "phone": search_phone})

@login_required
def sign_index(request, eid):
    event = get_object_or_404(Event, id=eid)
    guest_list = Guest.objects.filter(event_id=eid)
    guest_data = str(len(guest_list))  # 签到人数
    sign_data = 0                      # 已签到人数
    for guest in guest_list:
        if guest.sign == True:
            sign_data += 1
    return render(request, 'sign_index.html', {'event': event,
                                               'guest': guest_data,
                                               'sign': sign_data})

# 前端签到页面
def sign_index2(request,eid):
    event_name = get_object_or_404(Event, id=eid)
    return render(request, 'sign_index2.html',{'eventId': eid,
                                               'eventNanme': event_name})

@login_required
def sign_index_action(request, eid):
    event = get_object_or_404(Event, id=eid)
    guest_list = Guest.objects.filter(event_id=eid)
    guest_data = str(len(guest_list))
    sign_data = 0
    for guest in guest_list:
        if guest.sign == True:
            sign_data += 1

    phone = request.POST.get('phone', '')
    result = Guest.objects.filter(phone=phone)
    if not result:
        return render(request, 'sign_index.html', {'event': event,
                                                   'hint': 'phone error.',
                                                   'guest': guest_data,
                                                   'sign': sign_data})

    result = Guest.objects.filter(phone=phone, event_id=eid)
    if not result:
        return render(request, 'sign_index.html', {'event': event,
                                                   'hint': 'event id or phone error.',
                                                   'guest': guest_data,
                                                   'sign': sign_data})

    result = Guest.objects.get(phone=phone, event_id=eid)
    if result.sign:
        return render(request, 'sign_index.html', {'event': event,
                                                   'hint': 'user has sign in.',
                                                   'guest': guest_data,
                                                   'sign': sign_data})
    else:
        Guest.objects.filter(phone=phone, event_id=eid).update(sign='1')
        return render(request, 'sign_index.html', {'event': event,
                                                   'hint': 'sign in success!',
                                                   'guest': guest_data,
                                                   'sign': str(int(sign_data)+1),
                                                   'user': result})

@login_required
def logout(request):
    auth.logout(request)
    response = HttpResponseRedirect('/index/')
    return response

