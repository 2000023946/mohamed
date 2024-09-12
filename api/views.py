from django.shortcuts import render

from rest_framework import generics

from welcome_page.models import *
from posts.models import *
from .serializer import *

from .perm_auth import PermissionsAndAuthentication

# Create your views here.

class RecentBase(PermissionsAndAuthentication, generics.GenericAPIView):
    queryset = Recent.objects.all()
    serializer_class = RecentSerializer

class RecentListAPIView(RecentBase, generics.ListAPIView):
    """
    View to Retrieve and Destroy Recents
    """

class RecentMixinAPIView(RecentBase, generics.RetrieveAPIView):
    """
    View to Retrieve and Destroy Recents
    """

class BaseBlog(PermissionsAndAuthentication, generics.GenericAPIView):
    queryset = Blog.objects.all()
    serializer_class = BlogSerializer

class BlogListAPIView(BaseBlog, generics.ListAPIView):
    """
    View to List All Blogs
    """

class BlogMixinAPIView(generics.RetrieveAPIView):
    """
    View to Retrieve and Destroy Blogs
    """

class BaseMember(PermissionsAndAuthentication, generics.GenericAPIView):
    queryset = Member.objects.all()
    serializer_class = MemberSerializer

class MemberListAPIView(BaseMember, generics.ListAPIView):
    """
    View to List All Members
    """

class MemberMixinAPIView(BaseMember, generics.RetrieveAPIView, generics.DestroyAPIView):
    """
    View to Retrieve and Destroy Members
    """

class BaseRequest(PermissionsAndAuthentication, generics.GenericAPIView):
    queryset = Request.objects.all()
    serializer_class = RequestSerializer

class RequestListAPIView(BaseRequest, generics.ListAPIView):
    """
    View to List All Requests
    """

class RequestMixinAPIView(BaseRequest, generics.DestroyAPIView, generics.RetrieveAPIView):
    """
    View to Retrieve or Destroy All Requests
    """

class BasePost(PermissionsAndAuthentication, generics.GenericAPIView):
    queryset = Post.objects.all()
    serializer_class = PostSerializer

class PostListAPIView(BasePost, generics.ListAPIView):
    """
    View to List All Posts
    """

class PostMixinAPIView(BasePost, generics.RetrieveAPIView, generics.DestroyAPIView):
    """
    View to Retrieve and Destroy Posts
    """