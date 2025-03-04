"""
ASGI config for django_movie project.

It exposes the ASGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/5.1/howto/deployment/asgi/
"""
import os

from channels.auth import AuthMiddlewareStack
from channels.routing import ProtocolTypeRouter, URLRouter
from channels.security.websocket import AllowedHostsOriginValidator
from django.core.asgi import get_asgi_application

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'django_movie.settings')
"""Initiate Django ASGI application early to ensure the AppRegistry
is populated before importing code that may import ORM models.
"""

from chat.routing import websocket_urlpatterns

application = ProtocolTypeRouter(
    {
        'http': get_asgi_application(),
        'websocket': AllowedHostsOriginValidator(
            AuthMiddlewareStack(URLRouter(websocket_urlpatterns))
        ),
        # Just HTTP for now. (We can add other protocols later.)
    }
)

"""
#==== Cтарая версия (до Асинх Чата)
import os

from django.core.asgi import get_asgi_application

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'django_movie.settings')

application = get_asgi_application()
"""

