from django.urls import path
from . import consumers

websocket_urlpatterns=[
    path('ws/sc/<str:group_name_sc>/',consumers.MySyncConsumer.as_asgi()),
    path('ws/ac/<str:group_name_sc>/',consumers.MyAsyncConsumer.as_asgi()),

]


