from django.db import models
from django.core.cache import cache
from pymongo import MongoClient

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
    
class Temp(object):
    pass

class DataLayer(object):
    CONNECTION_STRING = 'mongodb://maciek:gosia1@ds039880.mongolab.com:39880/maciek'
    def __init__(self):
        self.client = MongoClient(DataLayer.CONNECTION_STRING)
        self.collection = self.client.maciek.users


    def AddUser(self, username, password):
        if not self.UserTaken(username):
            self.collection.insert({'username': username, 'password': password})        
        #cache.set(PREFIX + username, password)
    
    def UserTaken(self, username):
        result = self.collection.find_one({'username': username})
        if result:
            return True
        return False
        #return cache.get(PREFIX + username) != None
    
    def ValidatePassword(self, username, password):
        print 'username is ', username
        result = self.collection.find_one({'username': username})
        if not result:
            print 'no result'
            return False
        if not 'password' in result:
            print 'password not in result'
            return False
        print 'lets see if its equal'
        print result
        print result['password']
        print password
        return result['password'] == password

        #return cache.get(PREFIX + username) and cache.get(PREFIX + username) == password

