from channels.auth import AuthMiddlewareStack
from channels.routing import ProtocolTypeRouter, URLRouter
import MTapp.routing
# I wrote this code

application = ProtocolTypeRouter(
    {
        # (http->django views is added by default)
        "websocket": AuthMiddlewareStack(
            URLRouter(MTapp.routing.websocket_urlpatterns)
        ),
    }
)
# end of code I wrote
