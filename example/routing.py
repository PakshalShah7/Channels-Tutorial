from django.urls import re_path

from example.consumers import ChatConsumer

websocket_urlpatterns = [
    re_path(r"(?P<room_name>\w+)/$", ChatConsumer.as_asgi())
]
