from django.db import models
from django.contrib.auth.models import User  # Use Django's built-in User model

class Note(models.Model):
    owner = models.ForeignKey(User, on_delete=models.CASCADE)
    note_text = models.TextField(max_length=500)
    pub_date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.note_text
    

class User(models.Model):
    username = models.CharField(max_length=200)
    password = models.CharField(max_length=200)
    def __str__(self):
        return self.username
