import os
from django.urls import path
import django
from channels.http import AsgiHandler
from channels.routing import ProtocolTypeRouter, URLRouter
from notification.middlewares import QueryParamsMiddleware

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'vaidinventory.settings')
django.setup()
from notification.consumers import NotificationConsumer

application = ProtocolTypeRouter({
  "http": AsgiHandler(),
  "websocket": QueryParamsMiddleware(URLRouter([
    path("notification/", NotificationConsumer.as_asgi()),
  ])),
})
