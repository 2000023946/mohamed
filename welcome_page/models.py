from django.db import models
from django.contrib.auth.models import User
from posts.models import Blog, Member
from datetime import datetime

# Create your models here.
class Recent(models.Model):
    recent_blog = models.ForeignKey(Blog, on_delete=models.CASCADE, related_name="blog")
    date = models.DateField(default=datetime.today())
    user_for = models.ForeignKey(User, on_delete=models.CASCADE, related_name="recents")

