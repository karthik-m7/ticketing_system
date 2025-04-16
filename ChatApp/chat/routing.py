# ticket/routing.py
from django.urls import re_path
from . import consumers

websocket_urlpatterns = [
    re_path(r'ws/ticket/(?P<ticket_id>\d+)/$', consumers.TicketConsumer.as_asgi()),
]
