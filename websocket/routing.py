from django.urls import path

from . import consumers

websocket_urlpatterns = [
    path('ws/chat_room/<int:room_id>/', consumers.MyConsumer.as_asgi()),
    path('ws/request/<str:username>/', consumers.RequestConsumer.as_asgi())
]