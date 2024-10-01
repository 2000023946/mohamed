from django.contrib.auth.models import User
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.authtoken.models import Token

import json
from django.contrib.auth import authenticate
from posts.models import Member
# Create your views here.


class LoginView(APIView):
    permission_classes = []
    authentication_classes = []
    def post(self, request):
        data = json.loads(request.data)
        username, password = data.values()
        user = authenticate(request, username=username, password=password)
        if user is not None:
            member = Member.objects.get(user=user)
            token, created = Token.objects.get_or_create(user=user)
            return Response({'Success':True, "Response":'token', 'User_Id':user.id, 'Token':token.key})
        return Response({"Success": False, 'Response':'Invalid Credentials'})

    
class SignUpUserAPIView(APIView):
    permission_classes = []
    authentication_classes = []
    def post(self, request):
        data = json.loads(request.data)
        username, email, password, password2 = data.values()
        if not User.objects.filter(username=username).exists(): 
            if not User.objects.filter(email=email):
                if password == password2:
                    user = User.objects.create_user(username=username, email=email, password=password)
                    user.save()
                    member = Member(user=user)
                    member.save()
                    return Response({"Success":True, "Response":'New user created!'})
                return Response({"Success":False, 'Response': 'Passwords do not match!'})
            return Response({"Success": False, 'Response':'Mmail Already exists!'})
        return Response({"Success": False, 'Response':'Username already exists!'})
    