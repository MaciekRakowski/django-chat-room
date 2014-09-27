from django.db import models

# Create your models here.
class Greeting(models.Model):
    when = models.DateTimeField('date created', auto_now_add=True)


class User(models.Model):
    def __init__(self):
        self.name = None

    def IsLoggedIn(self):
        return self.name != None


def ValidatePassword(username, password):
    return password == 'password'
