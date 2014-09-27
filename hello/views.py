import pusher

from django.shortcuts import render
from django.http import HttpResponse

from django.core.context_processors import csrf
from django.shortcuts import render_to_response

from .models import Greeting
from .models import User
from .models import ValidatePassword

# Create your views here.

def GetUser(request):
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

    greeting = Greeting()
    greeting.save()

    greetings = Greeting.objects.all()

    return render(request, 'db.html', {'greetings': greetings})

