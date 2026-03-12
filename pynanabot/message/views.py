from pathlib import Path

from django.conf import settings
from rest_framework import permissions, viewsets
from rest_framework.response import Response

from .models import ReceivedMessage, SentMessage
from .serializers import ReceivedMessageSerializer, SentMessageSerializer
from .llm.reply import get_reply, should_reply
from .llm.profile import get_updated_profile
from .profile_store import read_profile, write_profile

BASE_DIR = Path(__file__).resolve().parent.parent.parent
SYSTEM_PROMPT_PATH = BASE_DIR / 'prompts' / 'system.md'
DECISION_PROMPT_PATH = BASE_DIR / 'prompts' / 'decision.md'


def _load_system_prompt() -> str:
    if SYSTEM_PROMPT_PATH.exists():
        return SYSTEM_PROMPT_PATH.read_text(encoding='utf-8')
    return '너는 단체 채팅방 봇이야. 자연스럽다고 판단될 때만 응답해. 아니면 아무것도 출력하지 마.'


def _load_decision_prompt() -> str:
    if DECISION_PROMPT_PATH.exists():
        return DECISION_PROMPT_PATH.read_text(encoding='utf-8')
    return '최근 대화를 보고 응답해야 하면 yes, 아니면 no만 출력해.'


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
            message=message,
        )

        # 같은 방의 최근 N개 메시지 (시간순, 봇 메시지 포함)
        received_qs = list(
            ReceivedMessage.objects
            .filter(room=room)
            .order_by('-created_at')[:settings.CONTEXT_MESSAGE_COUNT]
        )
        sent_qs = list(
            SentMessage.objects
            .filter(room=room)
            .order_by('-created_at')[:settings.CONTEXT_MESSAGE_COUNT]
        )
        combined = sorted(
            [{'sender': m.sender, 'message': m.message, 'created_at': m.created_at} for m in received_qs] +
            [{'sender': '[봇]', 'message': m.message, 'created_at': m.created_at} for m in sent_qs],
            key=lambda x: x['created_at']
        )
        context_messages = [
            {'sender': m['sender'], 'message': m['message']}
            for m in combined[-settings.CONTEXT_MESSAGE_COUNT:]
        ]

        sender_profile = read_profile(sender)
        system_prompt = _load_system_prompt()
        decision_prompt = _load_decision_prompt()

        # 호출 1: 응답 여부 판단
        do_reply = should_reply(
            context_messages=context_messages,
            decision_prompt=decision_prompt,
            model=settings.LLM_MODEL,
        )

        # 호출 2: 응답 생성
        reply_message = None
        if do_reply:
            candidate = get_reply(
                context_messages=context_messages,
                sender_profile=sender_profile,
                system_prompt=system_prompt,
                model=settings.LLM_MODEL,
            )
            if settings.BOT_REPLY_ENABLED:
                reply_message = candidate
                if reply_message:
                    print(f"[응답] \"{message}\" → {reply_message}")
                else:
                    print(f"[응답] \"{message}\" → (빈 응답)")
            else:
                if candidate:
                    print(f"[잠입모드] \"{message}\" → {candidate}")
                else:
                    print(f"[잠입모드] \"{message}\" → (빈 응답)")
        else:
            print(f"[판단] \"{message}\" → skip")

        # 호출 2: 프로필 갱신 (비활성화)
        # updated_profile = get_updated_profile(
        #     message=message,
        #     current_profile=sender_profile,
        #     model=settings.LLM_MODEL,
        # )
        # if updated_profile:
        #     write_profile(sender, updated_profile)

        if reply_message:
            SentMessage.objects.create(
                room=room,
                reply_to=received_message,
                message=reply_message,
            )

        return Response({
            'room': room,
            'message': reply_message,
        })
