from django.urls import re_path

from websocketControl.consumers import ControlConsumer

websocket_urlpatterns = [
        re_path(r'ws/control/', ControlConsumer)
]

