from rest_framework import serializers

from welcome_page.models import *
from posts.models import *

class UserSerializer(serializers.Serializer):
    user = serializers.SerializerMethodField('get_user')

    def get_user(self, user_id):
        return  [
            {'user_id': user_id},
            {'username': User.objects.get(id=user_id).username},
            {'user_url': f'http://127.0.0.1:8000/api/member/{user_id}'}
        ]
    
    @staticmethod
    def run_dict(dict, data):
        data = data['user']
        for pair in data:
            key, value = zip(*pair.items())
            dict[key[0]] = value[0]
    
class BlogInfoSerializer(serializers.Serializer):
    blog = serializers.SerializerMethodField('get_blog')
    
    def get_blog(self, blog_id):
        return  {
            'blog_id' : blog_id,
            'title' : Blog.objects.get(id=blog_id).username,
            'blog_url' : f'http://127.0.0.1:8000/api/member/{blog_id}'
        }
        

class RecentSerializer(serializers.ModelSerializer):
    recent_id = serializers.SerializerMethodField()
    recent_url = serializers.SerializerMethodField()
    class Meta:
        attr = ['recent_id', 'recent_url', 'recent_blog', 'date', 'user_for']
        model = Recent
        fields = attr
        read_only_fields = attr

    def get_recent_url(self, obj):
        return f'http://127.0.0.1:8000/api/recent/{obj.id}'

    def get_recent_id(self, obj):
        return obj.id if obj.id else None

    def to_representation(self ,instance):
        dict = super().to_representation(instance)
        blog_id = dict['recent_blog']
        user_id = dict['user_for']
        dict['recent_blog'] = {
            'blog_id' : blog_id,
            'blog_title' : Blog.objects.get(id=blog_id).title,
            'blog_url' : f'http://127.0.0.1:8000/api/blog/{blog_id}'
        }
        user_dict = UserSerializer(user_id).data
        dict['user_for'] = {}
        UserSerializer.run_dict(dict['user_for'], user_dict)
        return dict

class MemberSerializer(serializers.ModelSerializer):
    class Meta:
        model = Member
        fields = ['id','user','blog']
        read_only_fields = ['user','blog']
    
    def get_id(self, value):#first to ids are switched 
        if value == 1:
            return 2
        if value == 2:
            return 1
        return value

    def to_representation(self, instance):
        dict = super().to_representation(instance)
        user_id = self.get_id(dict['user'])
        data = UserSerializer(user_id).data
        dict['user'] = {}
        UserSerializer.run_dict(dict['user'], data)
        blog_list = dict['blog']
        list = []
        for blog_id in blog_list:
            list.append({'blog_id':blog_id, 'blog_url': f'http://127.0.0.1:8000/api/blog/{blog_id}'})
        dict['blog'] = list
        return dict
    

class BlogSerializer(serializers.ModelSerializer):
    blog_id = serializers.SerializerMethodField('get_blog_id')
    state = serializers.SerializerMethodField('get_state')
    class Meta:
        model = Blog
        fields = ['blog_id','post', 'title', 'description', 'created_user', 'date', 'number_users', 'state']
        read_only_fields = ['post', 'title', 'description',
                         'created_user', 'date', 'number_users', 'state']
        
    def get_state(self, obj):
        if obj.state:
            return "Public"
        return "Private"
        
    def get_blog_id(self, obj):
        return obj.id

    def to_representation(self, instance):
        dict = super().to_representation(instance)
        
        post_list = dict['post']
        list = []
        for post in post_list:
            list.append({"post_id": post, "post_url":f'http://127.0.0.1:8000/api/post/{post}'})
        dict['post'] = list

        user_id = dict['created_user']
        dict['created_user'] = UserSerializer(user_id).data
        return dict
    

class RequestSerializer(serializers.ModelSerializer):
    request = serializers.SerializerMethodField('get_request')
    blog = serializers.SerializerMethodField('get_blog')
    status = serializers.SerializerMethodField('get_status')
    class Meta:
        model = Request
        fields = ['request', 'user_from', 'blog', 'user_to', 'status']
        read_only_fields = ['request', 'user_from', 'blog', 'user_to', 'status']

    def get_request(self, obj):
        return {
            "reqeust_id": obj.id,
            "request_url": f'http://127.0.0.1:8000/api/request/{obj.id}'
        }
    
    def get_blog(self, obj):
        return {
            "blog_id" : obj.blog.id,
            "title": obj.blog.title,
            "blog_url": f'http://127.0.0.1:8000/api/blog/{obj.blog.id}'
        }
    
    def get_status(self, obj):
        if obj.status == 0:
            return f'Pending'
        elif obj.status == 1:
            return f'Accepted'
        elif obj.status == 2:
            return f'Declined'
    

    def to_representation(self, instance):
        dict =  super().to_representation(instance)
        id = {'user_from': dict['user_from'], 'user_to':dict['user_to']}

        dict['user_from'] = {}
        data = UserSerializer(id['user_from']).data
        UserSerializer.run_dict(dict['user_from'], data)

        dict['user_to'] = {}
        data = UserSerializer(id['user_to']).data
        UserSerializer.run_dict(dict['user_to'], data)

        return dict

class PostSerializer(serializers.ModelSerializer):
    user_url = serializers.SerializerMethodField('get_user_url')
    class Meta:
        model = Post
        fields = '__all__'
        read_only_fields = ['username', 'txt_message', 'date']

    def get_user_url(self, obj):
        user = User.objects.get(username=obj.username)
        user_id = user.id
        return f'http://127.0.0.1:8000/api/member/{user_id}'
