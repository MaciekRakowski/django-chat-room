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
        self.CurrentChatRoom = ''
        #self.
 
    def IsLoggedIn(self):
        return self.LoggedIn
    
class ChatRoom(object):
    def __init__(self, name, id):
        self.Name = name
        self.Id = id
        self.users = []

class DataLayer(object):
    CONNECTION_STRING = 'mongodb://maciek:gosia1@ds039880.mongolab.com:39880/maciek'
    def __init__(self):
        self.client = MongoClient(DataLayer.CONNECTION_STRING)
        self.users = self.client.maciek.users
        self.ChatRooms = self.client.maciek.chatrooms


    def AddUser(self, username, password, retypepassword):
        if len(password) < 6:
            return 'Password must be 5 Characters.'
        if password != retypepassword:
            return 'Passwords must match.'
        if (len(username) < 3):
            return 'Username must be at least 3 characters in length.'
        if self.UserTaken(username):
            return 'Username is taken'
        self.users.insert({'username': username, 'password': password})
        return '' 
    
    def _GenerateChatroomId(self, chatroomName):
        return chatroomName.replace(' ', '_')
    
    def AddChatRoom(self, chatroomName):
        print 'adding chatroom'
        chatroomId = self._GenerateChatroomId(chatroomName)
        print 'ID is ' + chatroomId
        result = self.ChatRooms.find_one({'id': chatroomId})
        print result
        if result:
            return 'The Chatroom {0} already exists.'.format(chatroomName)
        
        self.ChatRooms.insert({'name': chatroomName, 'id': chatroomId})
        return ''

    def GetAllChatRooms(self):
        allRooms = []
        defaultRoom = ChatRoom('default', 'default')
        allRooms.append(defaultRoom)
        for chatroom in self.ChatRooms.find():
            room = ChatRoom(chatroom['name'], chatroom['id'])
            allRooms.append(room)
        return allRooms
    
    def UserTaken(self, username):
        result = self.users.find_one({'username': username})
        if result:
            return True
        return False
        #return cache.get(PREFIX + username) != None
    
    def ValidatePassword(self, username, password):
        print 'username is ', username
        result = self.users.find_one({'username': username})
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

