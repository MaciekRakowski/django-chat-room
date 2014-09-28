import pusher

from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect
from django.core.context_processors import csrf
from django.shortcuts import render_to_response

#import psycopg2
import models
from .models import Greeting
from .models import User
from .models import ValidatePassword
from pip._vendor.requests.models import Response

from django.core.cache import cache

# Create your views here.

# Hackish login that will be replaced with either Heroku SSO, Facebook Login, or another proper login.
def GetUser(request):
    user = User()
    if request.method == 'POST':
        username = request.POST['username']
        if ValidatePassword(username, request.POST['password']):
            user.name = username
            user.LoggedIn = True
    elif request.method == 'GET':
        user.name = request.COOKIES.get('username', None)
    return user

def ValidateUser(request):
    user = User()
    if request.method == 'POST':
        username = request.POST['username']
        if ValidatePassword(username, request.POST['password']):
            user.name = username
    elif request.method == 'GET':
        user.name = request.COOKIES.get('username', None)
    return user

def index(request):
    #return render(request, 'pusher.html')
    user = GetUser(request)
    c = {'user': user}
    c.update(csrf(request))
    # ... view code here
    response = render_to_response("pusher.html", c)
    if user.name:
        response.set_cookie('authenticated', True)
        response.set_cookie('username', user.name)
        return response
    else:
        response = HttpResponseRedirect('/login')
        return response

def RegisterUser(username, password, retypepassword):
    if len(password) < 6:
        return 'Password must be 5 Characters.'
    if password != retypepassword:
        return 'Passwords must match.'
    if (len(username) < 6):
        return 'Username must be 6 characters in length.'
    if models.UserTaken(username):
        return 'Username is taken'
    models.AddUser(username, password)
    return ''    

def GetRegisterResponse(request):
    user = User()
    username = request.POST.get('username', '')
    user.name = username
    password = request.POST.get('password', '')
    retypepassword = request.POST.get('retypepassword', '')
    errormessage = RegisterUser(username, password, retypepassword)
    if errormessage:
        user.RegisterErrorMessage = errormessage
        args = {'user': user}
        args.update(csrf(request))
        response = render_to_response("login.html", args)
        return response
    # add user
    cache.set('user-' + user.name, password)
    response = HttpResponseRedirect('/')
    response.set_cookie('username', user.name)
    return response

def login(request):
    if request.POST.get('register', None):#Register User
        return GetRegisterResponse(request)

    username = request.POST.get('username', '')
    password = request.POST.get('password', '')
    print 'user is ' + username
    if username and models.ValidatePassword(username, password):
        response = HttpResponseRedirect('/')
        response.set_cookie('username', username)
        return response
    print 'did NOT validate'
    user = User()
    args = {'user': user}
    args.update(csrf(request))
    response = render_to_response("login.html", args)
    return response


def RegisterPusher(request):
    p = pusher.Pusher(
	  app_id='90808',
	  key='373a11faaef13cc238f8',
	  secret='257d521aeb17e184b501'
    )
    #p['test_channel'].trigger('my_event', {'message': 'hello world'})
    #return HttpResponse('Registered!')    
    if request.method == 'POST':
        message = request.POST['themessage']
        print 'getting username'
        username = request.COOKIES.get('username', None)
        print 'username is ' + username
        message = '{0}: {1}'.format(username, message.replace('\n', '<br>'))
        p['test_channel'].trigger('onmessage', {'themessage': message})
    return HttpResponse('Registered!')  

def db(request):
    user = User()
    user.name = "maciek"
    cache.set("name", user)

    print cache.get("name").name
    
    value = request.GET.get('value', None)
    if (value):
        cache.set("key", value)
        return HttpResponse("value set to " + value) 
    else:
        value = cache.get("key") or '[none]'
        return HttpResponse("value read is " + value) 
     
