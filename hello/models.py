from django.db import models
from django.core.cache import cache

# Create your models here.
class Greeting(models.Model):
    #value = models.TextField('value', 'some value maciek')
#     def __init__(self):
#         super(Greeting, self).__init__()
    when = models.DateTimeField('date created', auto_now_add=True)


class User(models.Model):
    def __init__(self):
        super(User, self).__init__()
        self.name = ''
        self.LoggedIn = False
        self.RegisterErrorMessage = ''
        #self.
 
    def IsLoggedIn(self):
        return self.LoggedIn


PREFIX = 'user-'
def AddUser(username, password):
    cache.set(PREFIX + username, password)

def UserTaken(username):
    return cache.get(PREFIX + username) != None

def ValidatePassword(username, password):
    return cache.get(PREFIX + username) and cache.get(PREFIX + username) == password

