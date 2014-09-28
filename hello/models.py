from django.db import models

# Create your models here.
class Greeting(models.Model):
    #value = models.TextField('value', 'some value maciek')
#     def __init__(self):
#         super(Greeting, self).__init__()
    when = models.DateTimeField('date created', auto_now_add=True)


class User(models.Model):
    def __init__(self):
        super(User, self).__init__()
        self.name = None
        self.LoggedIn = False
        #self.
 
    def IsLoggedIn(self):
        return self.LoggedIn

class User2(models.Model):
    def __init__(self):
        super(User2, self).__init__()
        self.name = None
        self.LoggedIn = False
        #self.
 
    def IsLoggedIn(self):
        return self.LoggedIn
 
def ValidatePassword(username, password):
    return password == 'password'
