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
    recent_blog = serializers.SerializerMethodField()
    class Meta:
        attr = ['recent_id', 'recent_url', 'recent_blog', 'date', 'user_for']
        model = Recent
        fields = attr
        read_only_fields = attr

    def get_recent_url(self, obj):
        return f'http://127.0.0.1:8000/api/recent/{obj.id}'

    def get_recent_id(self, obj):
        return obj.id if obj.id else None
    
    def get_recent_blog(self, obj):
        return BlogSerializer(obj.recent_blog).data

    def to_representation(self ,instance):
        dict = super().to_representation(instance)
        blog_id = dict['recent_blog']
        user_id = dict['user_for']
        user_dict = UserSerializer(user_id).data
        dict['user_for'] = {}
        UserSerializer.run_dict(dict['user_for'], user_dict)
        return dict
    
class BlogSerializer(serializers.ModelSerializer):
    blog_id = serializers.SerializerMethodField('get_blog_id')
    state = serializers.SerializerMethodField('get_state')
    created_user = serializers.SerializerMethodField()
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
    
    def get_created_user(self, obj):
        return{
            'name':obj.created_user.username,
            'id':obj.created_user.id,
            'url':f'http://127.0.0.1:8000/api/member/{obj.created_user.id}'
        }

    def to_representation(self, instance):
        dict = super().to_representation(instance)
        post_list = dict['post']
        post_list = [{"post_id": post, "post_url":f'http://127.0.0.1:8000/api/post/{post}'} for post in dict['post']]
        dict['post'] = post_list
        return dict

class MemberSerializer(serializers.ModelSerializer):
    recents = serializers.SerializerMethodField()
    popular = serializers.SerializerMethodField()
    recommendation = serializers.SerializerMethodField()
    blogs = serializers.SerializerMethodField()
    class Meta:
        model = Member
        fields = ['id','user','blogs', 'recents', 'popular', 'recommendation']
        read_only_fields = ['user','blogs', 'recents', 'popular','recommendation']
    
    def get_id(self, value):#first to ids are switched 
        if value == 1:
            return 2
        if value == 2:
            return 1
        return value
    
    def get_blogs(self, obj):
        return BlogSerializer(obj.blog, many=True).data
    
    def get_recommendation(self, obj):
        recents = self.get_recents(obj)
        recommend = []
        for recent in recents:
            title =  recent['recent_blog']['title']
            recommend_queryset = Member.objects.recommend(title)
            all_blogs = BlogSerializer(recommend_queryset, many=True).data
            if all_blogs:
                recommend.append(all_blogs)
        return recommend
            

    def get_popular(self, obj):
        raw_data = Blog.objects.popular()
        data = BlogSerializer(raw_data, many=True).data
        return data

    def get_recents(self, obj):
        queryset = Member.objects.recent(obj.user.username)
        data = RecentSerializer(queryset, many=True).data 
        return data
    
    def to_representation(self, instance):
        dict = super().to_representation(instance)
        user_id = self.get_id(dict['user'])
        data = UserSerializer(user_id).data
        dict['user'] = {}
        UserSerializer.run_dict(dict['user'], data)

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
