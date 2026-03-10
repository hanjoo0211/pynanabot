from unittest.mock import patch, MagicMock
from django.test import TestCase
from pynanabot.message.llm.reply import get_reply


class GetReplyTest(TestCase):
    @patch('pynanabot.message.llm.reply.get_client')
    def test_returns_reply_when_llm_responds(self, mock_get_client):
        mock_client = MagicMock()
        mock_client.chat.completions.create.return_value = MagicMock(
            choices=[MagicMock(message=MagicMock(content='안녕!'))]
        )
        mock_get_client.return_value = mock_client

        result = get_reply(
            context_messages=[{'sender': '홍길동', 'message': '안녕'}],
            sender_profile='주식에 관심 많음',
            system_prompt='너는 봇이야.',
            model='test-model',
        )
        self.assertEqual(result, '안녕!')

    @patch('pynanabot.message.llm.reply.get_client')
    def test_returns_none_when_llm_returns_empty(self, mock_get_client):
        mock_client = MagicMock()
        mock_client.chat.completions.create.return_value = MagicMock(
            choices=[MagicMock(message=MagicMock(content=''))]
        )
        mock_get_client.return_value = mock_client

        result = get_reply(
            context_messages=[{'sender': '홍길동', 'message': '안녕'}],
            sender_profile='',
            system_prompt='너는 봇이야.',
            model='test-model',
        )
        self.assertIsNone(result)
