"""
ASGI config for MTproj project.

It exposes the ASGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/4.2/howto/deployment/asgi/
"""

import os
from django.core.asgi import get_asgi_application
from channels.routing import ProtocolTypeRouter, URLRouter
from channels.auth import AuthMiddlewareStack
import MTapp.routing

#I wrote this code

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "MTproj.settings")

application = ProtocolTypeRouter(
    {
        "http": get_asgi_application(),
        "websocket": AuthMiddlewareStack(
            URLRouter(MTapp.routing.websocket_urlpatterns)
        ),
    }
)
# end of code I wrote
