from rest_framework import permissions, viewsets
from rest_framework.response import Response

from ..settings import env
from .models import ReceivedMessage, SentMessage
from .serializers import ReceivedMessageSerializer, SentMessageSerializer
from .teams_workflow.text import teams_text_message


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
        reply_room = room # 기본값은 메시지 받은 방으로 설정

        # TODO: 메시지 분기 필요
        if not is_group_chat or room == env('BANANA_GROUPTALK'):
            if "시치" in message:
                words = message.split()
                for word in words:
                    if "시치" in word:
                        prior_sic = word.split("시치")[0]
                        if not prior_sic:
                            prior_sic = "페리"
                        reply_message = f"아오 {prior_sic}시치"
                        
        # 오픈채팅 주식 공지
        if message.startswith("# ") and room == env('LG_STOCKS_ROOM'):
            message += "..."
            try:
                teams_text_message(
                    url=env('TEAMS_TEST_URL'),
                    message=message
                )
            except Exception as e:
                print(e)
            reply_room = env('BANANA_GROUPTALK')
            reply_message = message
  
        # 메시지 저장
        if reply_message:
            SentMessage.objects.create(
                room=reply_room,
                reply_to=received_message,
                message=reply_message
            )
        
        return Response({
            "room": reply_room,
            "message": reply_message
        })
