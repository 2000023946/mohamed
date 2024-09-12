from django.urls import path
from . import views

urlpatterns = [
    path('recent/',views.RecentListAPIView.as_view()),
    path('blog/', views.BlogListAPIView.as_view()),
    path('request/', views.RequestListAPIView.as_view()),
    path('member/', views.MemberListAPIView.as_view()),
    path('post/', views.PostListAPIView.as_view()),
    path('blog/<int:pk>', views.BlogMixinAPIView.as_view()),
    path('member/<int:pk>', views.MemberMixinAPIView.as_view()),
    path('request/<int:pk>', views.RequestMixinAPIView.as_view()),
    path('post/<int:pk>', views.PostMixinAPIView.as_view()),
    path('recent/<int:pk>',views.RecentMixinAPIView.as_view()),
    path('blog/popular',views.PopularAPIView.as_view()),
    path('blog/search/', views.BlogSearchAPIView.as_view()),
    path('recent/<str:username>/', views.MemberRecentAPIView.as_view()),
    path('recent/<str:username>/recommend', views.MemberRecentRecommendAPIView.as_view())
]

