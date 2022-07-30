from django.urls import re_path
from .consumers import ChatConsumer
from . import consumers_fail

websocket_urlpatterns = [
    re_path(r'ws/chat/(?P<room_name>\w+)/$', ChatConsumer.as_asgi()),
]

# websocket_urlpatterns = [
#     re_path(r'^ws/chat/(?P<room_name>[^/]+)/$', ChatConsumer),
# ]
