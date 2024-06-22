from django.urls import re_path

from . import consumers
# I wrote this code

websocket_urlpatterns = [
    re_path(r"ws/(?P<room_name>\w+)/$", consumers.ChatConsumer.as_asgi()),
]

# end of code I wrote
