from django.shortcuts import render

from rest_framework import generics
from rest_framework.views import APIView
from rest_framework.response import Response

from welcome_page.models import *
from posts.models import *
from .serializer import *
import requests

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

class BlogMixinAPIView(BaseBlog, generics.RetrieveAPIView):
    """
    View to Retrieve and Destroy Blogs
    """


class BlogSearchAPIView(APIView):
    def get(self, request):
        try:
            query = request.GET.get('q')
            queryset = Blog.objects.get_search(query)
            data = BlogSerializer(queryset, many=True).data
        except :
            data = {"Error":"Enter valid search. ex http://127.0.0.1:8000/api/blog/search/?q=your_search"}
        return Response(data)
    
class MemberRecentRecommendAPIView(APIView):
    def get(self, request, username):
        all_recents_resp = requests.get(f"http://127.0.0.1:8000/api/recent/{username}/")
        recents = all_recents_resp.json()
        all_blog_titles = []
        recommend = []
        for recent in recents:
            all_blog_titles.append(recent['recent_blog']['blog_title'])
        for title in all_blog_titles:
            search_resp = requests.get(f"http://127.0.0.1:8000/api/blog/search/?q={title}")
            search_data = search_resp.json()
            for search in search_data:
                title = search['title']
                if not str(title) in all_blog_titles:
                    recommend.append({"blog_title":title, "blog_url":f"http://127.0.0.1:8000/api/blog/search/?q={title}"})
        return Response(recommend)

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

class MemberRecentAPIView(APIView):
    
    def get(self, request, username):
        queryset = Member.objects.recent(username)
        data = RecentSerializer(queryset, many=True).data 
        return Response(data)


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

class PopularAPIView(APIView):
    def get(self, request):
        data = Blog.objects.popular()
        return Response(data)
        # return Response({"popular":data})