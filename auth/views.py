from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response
from django.contrib.auth.models import User
# Create your views here.


class LoginView(APIView):
    def post(self, request):
        username = request.POST.username
        password = request.POST.password
        for user in User.objects.all():
            if username == user.username and password == user.password:
                
                return Response()
        return Response({"Error": "Invalid Credentials"})
