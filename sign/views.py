from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect
from django.contrib import auth
from django.contrib.auth.decorators import login_required
from sign.models import Event, Guest
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger

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