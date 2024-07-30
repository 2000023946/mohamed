from django.db import models
from datetime import datetime
from django.contrib.auth.models import User
# Create your models here.

class Post(models.Model):
    username = models.CharField(max_length=100)
    txt_message = models.TextField()
    date = models.DateField(default=datetime.now())