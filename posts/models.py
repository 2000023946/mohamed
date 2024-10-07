from django.db import models
from datetime import date
from home.models import Post
from django.contrib.auth.models import User
from django.db.models import Q

# Create your models here.

class BlogQuerySet(models.QuerySet):
    def get_search_query(self, query):
        lookup = Q(Q(title__icontains=query) | Q(description__icontains=query))
        return self.filter(lookup)
    def get_member_query(self, query):
        blog = Blog.objects.get(id=query)
        return  blog.members.all()


class BlogManager(models.Manager):
    def get_queryset(self) -> models.QuerySet:
        return BlogQuerySet(model=self.model, using=self._db)
    
    def popular(self):
        return self.get_queryset().order_by('number_users')[:5]

    def get_search(self, query):
        return self.get_queryset().get_search_query(query)
    
    def get_members(self, query):
        return self.get_queryset().get_member_query(query)

                    
        


class Blog(models.Model):
    post = models.ManyToManyField(Post)
    title = models.CharField(max_length=100)
    description = models.CharField(max_length=200)
    created_user = models.ForeignKey(User, on_delete=models.CASCADE, default=1)
    date = models.DateField(default=date.today(), blank=True)
    number_users = models.IntegerField(default=0)
    state = models.BooleanField(default=True)
    objects = BlogManager()
    def __str__(self):
        return f"blog called {self.title} and users:{self.number_users}"
    
class MemberQuerySet(models.QuerySet):
    def get_user_query(self, username):
        user = User.objects.get(username=username)
        return user.recents.all().order_by('-id')[:5]
    def get_blog_query(self, blog_title):
        queryset_pool = Blog.objects.exclude(title__exact=blog_title)
        return queryset_pool.filter(title__contains=blog_title)
    def get_request_query(self, user_id):
        member = Member.objects.get(id=user_id)
        return member.acceptors.filter(status=0)
    def get_request_made_query(self, user_id):
        member = Member.objects.get(id=user_id)
        return member.requestors.filter(status=0)


class MemberManager(models.Manager):
    def get_queryset(self) -> models.QuerySet:
        return MemberQuerySet(model=self.model, using=self._db)
    def recent(self, username):
        return self.get_queryset().get_user_query(username)
    def recommend(self, blog_title):
        return self.get_queryset().get_blog_query(blog_title)
    def request(self, user_id):
        return self.get_queryset().get_request_query(user_id)
    def request_made(self, user_id):
        return self.get_queryset().get_request_made_query(user_id)


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
    