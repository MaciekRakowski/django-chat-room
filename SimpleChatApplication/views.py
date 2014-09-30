import pusher

from django.http import HttpResponse, HttpResponseRedirect
from django.core.context_processors import csrf
from django.shortcuts import render_to_response

#import psycopg2
import SimpleChatApplication
from SimpleChatApplication.models import User

from django.core.cache import cache

from pymongo import MongoClient




# Create your views here.
DATALAYER = None
# Hackish login that will be replaced with either Heroku SSO, Facebook Login, or another proper login.
def GetDataLayer():
    #key = "datalayer"
    global DATALAYER
    value = DATALAYER#cache.get(key)
    if value:
        print 'getting cached data layer'
        return value
    print 'no cached data layer'
    datalayer = SimpleChatApplication.models.DataLayer()
    
    print 'done setting temp'
    DATALAYER = datalayer
    #cache.set(key, datalayer)
    print 'done setting data layer'
    return datalayer

def GetUser(request):
    user = User()
    print 'getting data layer'
    datalayer = GetDataLayer()
    print 'got data layer'
    if request.method == 'POST':
        username = request.POST['username']
        if datalayer.ValidatePassword(username, request.POST['password']):
            user.name = username
            user.LoggedIn = True
    elif request.method == 'GET':
        user.name = request.COOKIES.get('username', None)    
    return user

def Logout(request):
    # TODO: Fix hackish hackish logout.
    response = HttpResponseRedirect('/login')
    response.delete_cookie('username')
    return response

def ValidateUser(request):
    user = User()
    datalayer = GetDataLayer()
    if request.method == 'POST':
        username = request.POST['username']
        if datalayer.ValidatePassword(username, request.POST['password']):
            user.name = username
    elif request.method == 'GET':
        user.name = request.COOKIES.get('username', None)
    return user

def index(request):
    #return render(request, 'pusher.html')
    user = GetUser(request)
    chatroom = request.GET.get('chatroom', 'default')
    user.CurrentChatRoom = chatroom
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
    datalayer = GetDataLayer()
    return datalayer.AddUser(username, password, retypepassword)

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
    #response = HttpResponseRedirect('/')
    response = HttpResponseRedirect('/ShowChatRooms')
    response.set_cookie('username', user.name)
    return response

def login(request):
    if request.method == 'POST':
        if request.POST.get('register', None):#Register User
            return GetRegisterResponse(request)
    
        username = request.POST.get('username', '')
        password = request.POST.get('password', '')
        datalayer = GetDataLayer()
        print 'user is ' + username
        if username and datalayer.ValidatePassword(username, password):
            response = HttpResponseRedirect('/ShowChatRooms')
            response.set_cookie('username', username)
            return response
        print 'did NOT validate'
        user = User()
        user.name = username
        user.RegisterErrorMessage = 'Invalid name/password combination.'
        args = {'user': user}
        args.update(csrf(request))
        response = render_to_response("login.html", args)
        return response
    else:
        args = {'user': User()}
        args.update(csrf(request))
        response = render_to_response("login.html", args)
        return response

def DrawLineEvent(request):
    print 'On Draw Line Event.'
    p = pusher.Pusher(
      app_id='90808',
      key='373a11faaef13cc238f8',
      secret='257d521aeb17e184b501'
    )
    if request.method == 'POST':
        theline = request.POST['theline']
        chatroom = request.POST.get('chatroom', None)
        if not chatroom:
            return HttpResponse('select chat room')        
        username = request.COOKIES.get('username', None)
        print 'the line is ' + theline + ' for user ' + username
        #message = '{0}: {1}'.format(username, message.replace('\n', '<br>'))
        p['test_channel'].trigger('onmessage-{0}-draw'.format(chatroom), {'theline': theline, 'username': username})
    return HttpResponse('Drew Line!')  

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
        chatroom = request.POST.get('chatroom', None)
        if not chatroom:
            return HttpResponse('select chat room')
        print 'getting username'
        username = request.COOKIES.get('username', None)
        print 'username is ' + username
        message = '{0}: {1}'.format(username, message.replace('\n', '<br>'))
        p['test_channel'].trigger('onmessage-' + chatroom, {'themessage': message})
    return HttpResponse('Registered!')  

def GetValue(collection, key):
    result = collection.find_one({'key': key})
    if not result:
        return ''
    if 'value' in result:
        return result['value']
    return ''

def db(request):
    client = MongoClient('mongodb://maciek:gosia1@ds039880.mongolab.com:39880/maciek')
    db = client.maciek
    collection = db.key_value_pairs    
    value = request.GET.get('value', None)
    if value:
        collection.insert({'key': 'name', 'value': value})
        return HttpResponse("value set to " + value) 
    else:
        value = GetValue(collection, 'name')
        if not value:
            value = '[None]'
        return HttpResponse("value read is " + value)
        
def ShowChatRooms(request):
    print 'on show chat rooms...'
    datalayer = GetDataLayer()
    args = {}
    args['message'] = ''
    args.update(csrf(request))
    if request.method == 'POST':
        chatroom = request.POST.get('chatroom', None)
        if (chatroom == 'default'):
            args['message'] = 'Cannot add default chatroom'
            return render_to_response("ShowChatRooms.html", args)
        message = datalayer.AddChatRoom(chatroom)        
        args['message'] = message if message else 'Chatoom "%s" Successfully Added.' % chatroom
    chatRooms = datalayer.GetAllChatRooms()
    args['ChatRooms'] = chatRooms    
    response = render_to_response("ShowChatRooms.html", args)
    return response
        
        
