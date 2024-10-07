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
    allowed_users = serializers.SerializerMethodField()
    class Meta:
        model = Blog
        fields = ['blog_id','post', 'title', 'description', 'created_user', 'date', 'number_users', 'state', 'allowed_users']
        read_only_fields = ['post', 'date', 'number_users', 'state', 'state']
        
    def get_state(self, obj):
        if obj.state:
            return "Public"
        return "Private"
        
    def get_blog_id(self, obj):
        return obj.id
    
    def get_allowed_users(self, obj):
        members = Blog.objects.get_members(self.get_blog_id(obj))
        return MemberInfoSerializer(members, many=True).data

    
    def get_created_user(self, obj):
        return{
            'name':obj.created_user.username,
            'id':obj.created_user.id,
            'url':f'http://127.0.0.1:8000/api/member/{obj.created_user.id}'
        }

    def to_representation(self, instance):
        dict = super().to_representation(instance)
        try:
            post_list = dict['post']
            post_list = [{"post_id": post, "post_url":f'http://127.0.0.1:8000/api/post/{post}'} for post in dict['post']]
            dict['post'] = post_list
        except TypeError:
            """"""
        return dict


class MemberSerializer(serializers.ModelSerializer):
    recents = serializers.SerializerMethodField()
    popular = serializers.SerializerMethodField()
    recommendation = serializers.SerializerMethodField()
    blogs = serializers.SerializerMethodField()
    request = serializers.SerializerMethodField()
    request_made = serializers.SerializerMethodField()
    class Meta:
        model = Member
        fields = ['id','request','user','blogs', 'recents', 'popular', 'recommendation', 'request_made']
        read_only_fields = ['user','reqeust', 'blogs', 'recents', 'popular','recommendation', 'request_made']
    
    def get_id(self, value):#first to ids are switched 
        if value == 1:
            return 2
        if value == 2:
            return 1
        return value
    
    def get_request_made(self, obj):
        requests = Member.objects.request_made(obj.id)
        return RequestSerializer(requests, many=True).data

    
    def get_request(self, obj):
        requests = Member.objects.request(obj.id)
        return RequestSerializer(requests, many=True).data
    
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
    
class MemberInfoSerializer(serializers.ModelSerializer):
    username = serializers.SerializerMethodField()
    class Meta:
        model = Member
        fields = ['id','username']
        read_only_fields = ['username', 'id']
    
    def get_username(self, obj):
        return obj.user.username
    
    def to_representation(self, instance):
        data = super().to_representation(instance)
        id = data['id']
        if id < 3:
            data['id'] = 1 if id == 2 else 2
        return data
    

class RequestSerializer(serializers.ModelSerializer):
    blog = serializers.SerializerMethodField('get_blog')
    status = serializers.SerializerMethodField('get_status')
    class Meta:
        model = Request
        fields = ['id', 'user_from', 'blog', 'user_to', 'status']

    
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
        read_only_fields = ['date']

    def get_user_url(self, obj):
        user = User.objects.get(username=obj.username)
        user_id = user.id
        return f'http://127.0.0.1:8000/api/member/{user_id}'


class BlogPostInfoSerializer(BlogSerializer):
    post = serializers.SerializerMethodField()
    

    def get_post(self, obj):
        print(obj)
        posts = PostSerializer(obj.post, many=True).data
        return posts