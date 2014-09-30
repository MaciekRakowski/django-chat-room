from django.db import models
from pymongo import MongoClient
import mysite


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
 
    def IsLoggedIn(self):
        return self.LoggedIn
    
class ChatRoom(object):
    def __init__(self, name, inId):
        self.Name = name
        self.Id = inId
        self.users = []

class DataLayer(object):
    CONNECTION_STRING = mysite.settings.CONNECTION_STRING
    def __init__(self):
        self.client = MongoClient(DataLayer.CONNECTION_STRING)
        self.users = self.client.maciek.users
        self.ChatRooms = self.client.maciek.chatrooms
        self.ChatroomLines = self.client.maciek.chatroomlines

    def AddLineToChatRoom(self, chatroom, lineData):
        result = self.ChatroomLines.find_one({'chatroom': chatroom})
        if not result:
            self.ChatroomLines.insert({'chatroom': chatroom, 'linedata': lineData})
            return
        currentLineData = result['linedata']
        currentLineData += ';' + lineData
        self.ChatroomLines.update({'chatroom': chatroom}, {'$set': {'linedata': currentLineData}})
    
    def GetLinesFromChatRoom(self, chatroom):
        result = self.ChatroomLines.find_one({'chatroom': chatroom})
        if not result:
            return ''
        return result['linedata']
    
    def ClearLinesInChatroom(self, chatroom):
        self.ChatroomLines.remove({'chatroom': chatroom})

    def AddUser(self, username, password, retypepassword):
        if len(password) < 6:
            return 'Password must be 6 Characters.'
        if password != retypepassword:
            return 'Passwords must match.'
        if (len(username) < 2):
            return 'Username must be at least 2 characters in length.'
        if self.UserTaken(username):
            return 'Username is taken'
        self.users.insert({'username': username, 'password': password})
        return '' 
    
    def _GenerateChatroomId(self, chatroomName):
        return chatroomName.replace(' ', '_')
    
    def AddChatRoom(self, chatroomName):
        chatroomId = self._GenerateChatroomId(chatroomName)
        result = self.ChatRooms.find_one({'id': chatroomId})
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
    
    def ValidatePassword(self, username, password):
        result = self.users.find_one({'username': username})
        if not result:
            return False
        if not 'password' in result:
            return False
        return result['password'] == password
