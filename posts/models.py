from django.db import models
from datetime import datetime
from home.models import Post
from django.contrib.auth.models import User
from django.db.models import Q

# Create your models here.

class BlogQuerySet(models.QuerySet):
    def get_search_query(self, query):
        lookup = Q(Q(title__icontains=query) | Q(description__icontains=query))
        return self.filter(lookup)


class BlogManager(models.Manager):
    def get_queryset(self) -> models.QuerySet:
        return BlogQuerySet(model=self.model, using=self._db)
    
    def popular(self):
        list = []
        for blog in Blog.objects.all():
            new_data = {"blog_id":blog.id, "users":blog.number_users, "blog_url":f'http://127.0.0.1:8000/api/blog/{blog.id}'}
            if len(list) <= 5:
                list.append(new_data)
            else:
                if list[len(list)-1]['users'] < new_data['users']:
                    list.append(new_data)
                else:
                    continue
            if len(list) == 1:
                continue
            else:
                lo = len(list)-1
                po = lo-1
                while po >= 0 and list[lo]['users'] > list[po]['users']:
                    cur = list[lo]
                    list[lo] = list[po]
                    list[po] = cur
                    po-= 1
                    lo -=1
            if len(list) > 6:
                list.pop()
        return list
        #return self.get_queryset().order_by('number_users')[:5]

    def get_search(self, query):
        return self.get_queryset().get_search_query(query)

                    
        


class Blog(models.Model):
    post = models.ManyToManyField(Post)
    title = models.CharField(max_length=100)
    description = models.CharField(max_length=200)
    created_user = models.ForeignKey(User, on_delete=models.CASCADE, default=1)
    date = models.DateField(default=datetime.now(), blank=True)
    number_users = models.IntegerField(default=0)
    state = models.BooleanField(default=True)
    objects = BlogManager()
    def __str__(self):
        return f"blog called {self.title} and users:{self.number_users}"
    
class MemberQuerySet(models.QuerySet):
    def get_user_query(self, username):
        user = User.objects.get(username=username)
        return user.recents.all()

class MemberManager(models.Manager):
    def get_queryset(self) -> models.QuerySet:
        return MemberQuerySet(model=self.model, using=self._db)
    def recent(self, username):
        return self.get_queryset().get_user_query(username)


class Member(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    blog = models.ManyToManyField(Blog, related_name="members", blank=True)
    objects = MemberManager()
    def __str__(self):
        return f"{self.user.username}"
class Request(models.Model):
    user_from = models.ForeignKey(Member, on_delete=models.CASCADE, related_name="requestors")
    blog = models.ForeignKey(Blog, on_delete=models.CASCADE)
    user_to = models.ForeignKey(Member, on_delete=models.CASCADE, related_name="acceptors")
    status = models.IntegerField(default=0)#0-> pending, 1->Accepted, 2->Declined
    def __str__(self) -> str:
        return f"user from {self.user_from} , blog {self.blog} user_to is {self.user_to} and id of {self.id}"
    