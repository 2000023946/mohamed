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

class RecentListAPIView(RecentBase, generics.ListCreateAPIView):
    """
    View to Retrieve and Destroy Recents
    """
    def post(self, request):
        data = request.data
        user_for_id, blog_id = data.values()
        if int(user_for_id) < 3:
            user_for_id = 1 if user_for_id == 2 else 2
        user_for = User.objects.get(id=user_for_id)
        recent_blog = Blog.objects.get(id=blog_id)
        if Recent.objects.filter(recent_blog=recent_blog, user_for=user_for).exists():
            return Response({'recent_id':-1})
        recent = Recent.objects.create(user_for=user_for, recent_blog=recent_blog)
        recent.save()
        serialized_data = RecentSerializer(recent).data
        return Response(serialized_data)

class RecentMixinAPIView(RecentBase, generics.RetrieveAPIView):
    """
    View to Retrieve and Destroy Recents
    """

class BaseBlog(PermissionsAndAuthentication, generics.GenericAPIView):
    queryset = Blog.objects.all()
    serializer_class = BlogSerializer

class BlogListAPIView(BaseBlog, generics.ListCreateAPIView):
    """
    View to List All Blogs
    """

class BlogMixinAPIView(BaseBlog, generics.RetrieveAPIView, generics.UpdateAPIView):
    """
    View to Retrieve and Destroy Blogs
    """
    def put(self, request, pk):
        data = request.data
        print(data['data'].keys())

        blog_id = data['data']['data']['blog']['blog_id']
        member_id = data['data']['data']['user_from']['user_id']
        blog = Blog.objects.get(id=blog_id)
        member = Member.objects.get(id=member_id)
        member.blog.add(blog)
        member_data = MemberSerializer(member).data
        return Response(member_data)



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

class MemberRecentAPIView(APIView, PermissionsAndAuthentication):
    permission_classes = []
    authentication_classes = []
    def get(self, request, username):
        queryset = Member.objects.recent(username)
        data = RecentSerializer(queryset, many=True).data 
        return Response(data)


class BaseRequest(PermissionsAndAuthentication, generics.GenericAPIView):
    queryset = Request.objects.all()
    serializer_class = RequestSerializer

class RequestListAPIView(BaseRequest, generics.ListCreateAPIView):
    """
    View to List All Requests
    """
    def post(self, request):
        user_from, user_to, blog = request.data.values()
        user_from = Member.objects.get(id=user_from)
        user_to = Member.objects.get(id=user_to)
        blog = Blog.objects.get(id=blog)
        request = Request.objects.create(user_from=user_from, user_to=user_to, blog=blog)
        request.save()
        serialized_data = RequestSerializer(request).data
        return Response(serialized_data)
    
class RequestMixinAPIView(BaseRequest, generics.DestroyAPIView, generics.RetrieveAPIView, generics.UpdateAPIView):
    """
    View to Retrieve or Destroy All Requests
    """
    def put(self, request, pk):
        data = request.data
        print(data)
        is_accepted = data['is_accepted']
        request = Request.objects.get(id=pk)
        if is_accepted:#add the user to the blog if accepted
            request.status = 1
            user_from = request.user_from
            user_from.blog.add(request.blog)
            user_from.save()
        else:
            request.status = 2
        request.save()
        serialized_data = RequestSerializer(request).data
        return Response(serialized_data)

class BasePost(PermissionsAndAuthentication, generics.GenericAPIView):
    queryset = Post.objects.all()
    serializer_class = PostSerializer

class PostListAPIView(BasePost, PermissionsAndAuthentication, generics.ListCreateAPIView):
    """
    View to List All Posts
    """
    def get(self, request):
        queryset = Post.objects.all()
        posts = PostSerializer(queryset, many=True).data
        return Response(posts)
    def post(self, request):
        data = request.data
        username, data_list = data.values()
        txt_message, blog_id = data_list.split(',')
        post = Post.objects.create(username=username, txt_message=txt_message)
        post.save()
        blog = Blog.objects.get(id=blog_id)
        blog.post.add(post)
        blog.save()
        return Response({'username':username, 'txt_message':txt_message, 'date':post.date})

class PostMixinAPIView(BasePost, generics.RetrieveAPIView, generics.DestroyAPIView, generics.UpdateAPIView):
    """
    View to Retrieve and Destroy Posts
    """
    def put(self, request, pk):
        data = request.data
        content = data['content']
        blog_id = data['blog_id']
        blog = Blog.objects.get(id=blog_id)
        post = Post.objects.get(id=pk)
        post.txt_message = content
        post.save()
        serialized_data = BlogSerializer(blog).data
        return Response(serialized_data)
    def delete(self, request, pk):
        data = request.data
        post = Post.objects.get(id=pk)
        post.delete()
        blog_id = data['blog_id']
        blog = Blog.objects.get(id=blog_id)
        serialized_data = BlogSerializer(blog).data
        return Response(serialized_data)

        
        
    


class PopularAPIView(APIView):
    def get(self, request):
        data = Blog.objects.popular()
        return Response(data)