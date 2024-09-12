from django.urls import path
from . import views

urlpatterns = [
    path("", views.index, name = "home"),
    path("logout", views.logout_user, name="logout"),
    path("requests",views.requests, name="requests"),
    path("search", views.search, name="search"),
    path("<int:pk>", views.blog_content, name = "blog_content"),
    path("<int:pk>/remove/<int:sk>", views.remove, name="remove"),
    path("<int:pk>/update/<int:sk>", views.update, name="update")
]