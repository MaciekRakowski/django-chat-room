import pusher

from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect
from django.core.context_processors import csrf
from django.shortcuts import render_to_response

#import psycopg2

from .models import Greeting
from .models import User
from .models import ValidatePassword
from pip._vendor.requests.models import Response

import datetime
import pymongo
from pymongo import MongoClient

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
    cerf = csrf(request)
    print cerf
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

def login(request):
    #if request.POST['register']:
        
    user = GetUser(request)
    if user.IsLoggedIn():
        return HttpResponseRedirect('/')
    else:
        return render_to_response("login.html", {'user': user}) 

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
    cache.set("key", "maciek rakowski")
    value = cache.get("key")
    
    return HttpResponse(value) 
#     print 'getting client'
#     client = MongoClient('mongodb://user:pass@server.compose.io/database_name')
#      
#     print 'getting db'
#     # Specify the database
#     db = client.mytestdatabase
#     # Print a list of collections
#     print db.collection_names()
#      
#     # Specify the collection, in this case 'monsters'
#     collection = db.monsters
#      
#     # Get a count of the documents in this collection
#     count = collection.count()
#     print "The number of documents you have in this collection is:", count
#      
#     # Create a document for a monster
#     monster = {"name": "Dracula",
#                "occupation": "Blood Sucker",
#                "tags": ["vampire", "teeth", "bat"],
#                "date": datetime.datetime.utcnow()
#                }
#      
#     # Insert the monster document into the monsters collection
#     monster_id = collection.insert(monster)
#      
#     # Print out our monster documents
#     for monster in collection.find():
#         print monster
#      
#     # Query for a particular monster
#     print collection.find_one({"name": "Dracula"})
#     return HttpResponse('done!') 

#     greeting = Greeting()
#     greeting.save()
# 
#     greetings = Greeting.objects.all()
# 
#     return render(request, 'db.html', {'greetings': greetings})

