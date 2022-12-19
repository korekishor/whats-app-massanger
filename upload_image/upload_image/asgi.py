 
import os

from django.core.asgi import get_asgi_application

from channels.routing import ProtocolTypeRouter,URLRouter
import upload_app.routing
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'upload_image.settings')


application=ProtocolTypeRouter({
    "http":get_asgi_application(),
    'websocket':URLRouter(
        upload_app.routing.websocket_urlpatterns
        
    )
    
    # just http for now (we can add other protocall here)
})

