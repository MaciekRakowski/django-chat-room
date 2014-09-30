import pusher

from django.http import HttpResponse, HttpResponseRedirect
from django.core.context_processors import csrf
from django.shortcuts import render_to_response

#import psycopg2
import SimpleChatApplication
from SimpleChatApplication.models import User

from django.core.cache import cache

from pymongo import MongoClient
import cgi



# Create your views here.
DATALAYER = None
# Hackish login that will be replaced with either Heroku SSO, Facebook Login, or another proper login.
def GetDataLayer():
    global DATALAYER
    value = DATALAYER
    if value:
        return value
    datalayer = SimpleChatApplication.models.DataLayer()
    
    DATALAYER = datalayer
    return datalayer

def GetUser(request):
    user = User()
    datalayer = GetDataLayer()
    if request.method == 'POST':
        username = request.POST['username']
        if datalayer.ValidatePassword(username, request.POST['password']):
            user.name = username
            user.LoggedIn = True
    elif request.method == 'GET':
        user.name = request.COOKIES.get('username', None)    
    return user

# Hackish login/logout/validate methods that need to go away.
def Logout(request):
    # TODO: Fix hackish hackish logout.
    response = HttpResponseRedirect('/login')
    response.delete_cookie('username')
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
        if username and datalayer.ValidatePassword(username, password):
            response = HttpResponseRedirect('/ShowChatRooms')
            response.set_cookie('username', username)
            return response
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
# End of Hackish login that will be replaced with either Heroku SSO, Facebook Login, or another proper login.

def index(request):
    user = GetUser(request)
    datalayer = GetDataLayer()
    chatroom = request.GET.get('chatroom', 'default')
    lines = datalayer.GetLinesFromChatRoom(chatroom)
    user.CurrentChatRoom = chatroom
    args = {'user': user}
    args['lines'] = lines
    args.update(csrf(request))
    # ... view code here
    response = render_to_response("ChatRoom.html", args)
    if user.name:
        response.set_cookie('authenticated', True)
        response.set_cookie('username', user.name)
        return response
    else:
        response = HttpResponseRedirect('/login')
        return response

def DrawLineEvent(request):
    p = pusher.Pusher(
      app_id='90808',
      key='373a11faaef13cc238f8',
      secret='257d521aeb17e184b501'
    )
    if request.method == 'POST':
        datalayer = GetDataLayer()
        chatroom = request.POST.get('chatroom', None)
        if not chatroom:
            return HttpResponse('select chat room')        
        username = request.COOKIES.get('username', None)
        if request.POST.get('ClearCanvas', None):
            
            datalayer.ClearLinesInChatroom(chatroom)
            p['test_channel'].trigger('onmessage-{0}-draw'.format(chatroom), {'ClearCanvas': 'True', 'username': username})
            return HttpResponse('Cleared Canvas!') 
        theline = request.POST['theline']
        datalayer.AddLineToChatRoom(chatroom, theline)

        p['test_channel'].trigger('onmessage-{0}-draw'.format(chatroom), {'theline': theline, 'username': username})
    return HttpResponse('Drew Line!')  

def PushMessages(request):
    p = pusher.Pusher(
	  app_id='90808',
	  key='373a11faaef13cc238f8',
	  secret='257d521aeb17e184b501'
    )

    if request.method == 'POST':
        message = request.POST['themessage']
        chatroom = request.POST.get('chatroom', None)
        if not chatroom:
            return HttpResponse('select chat room')
        username = request.COOKIES.get('username', None)
        message = cgi.escape(message)
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
        
def ShowChatRooms(request):
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

