from django.contrib import admin
from .models import Blog, Member, Request
# Register your models here.

admin.site.register(Blog)
admin.site.register(Member)
admin.site.register(Request)
