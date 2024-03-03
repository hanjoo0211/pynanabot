from django.urls import include, path
from rest_framework import routers

from pynanabot.message import views as message_views

router = routers.DefaultRouter()
router.register(r'received-messages', message_views.ReceivedMessageViewSet)
router.register(r'sent-messages', message_views.SentMessageViewSet)
router.register(r'reply', message_views.ReplyViewSet, basename='reply')

urlpatterns = [
    path('', include(router.urls)),
    path('api-auth/', include('rest_framework.urls', namespace='rest_framework'))
]

urlpatterns += router.urls
