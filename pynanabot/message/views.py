from .models import ReceivedMessage, SentMessage
from rest_framework import permissions, viewsets
from rest_framework.response import Response

from .serializers import ReceivedMessageSerializer, SentMessageSerializer


class ReceivedMessageViewSet(viewsets.ModelViewSet):
    queryset = ReceivedMessage.objects.all()
    serializer_class = ReceivedMessageSerializer
    permission_classes = [permissions.IsAuthenticated]


class SentMessageViewSet(viewsets.ModelViewSet):
    queryset = SentMessage.objects.all()
    serializer_class = SentMessageSerializer
    permission_classes = [permissions.IsAuthenticated]


class ReplyViewSet(viewsets.ViewSet):
    permission_classes = [permissions.IsAuthenticated]
    
    def create(self, request):
        room = request.data.get('room')
        sender = request.data.get('sender')
        is_group_chat = request.data.get('isGroupChat')
        message = request.data.get('message')
        received_message = ReceivedMessage.objects.create(
            room=room,
            sender=sender,
            is_group_chat=is_group_chat,
            message=message
        )

        reply_message = None

        # 메시지 분기 필요
        if "시치" in message:
            reply_message = "아오 페리시치"
        
        if reply_message:
            SentMessage.objects.create(
                room=room,
                reply_to=received_message,
                message=reply_message
            )
        
        return Response({"message": reply_message})
