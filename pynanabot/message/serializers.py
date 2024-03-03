from .models import ReceivedMessage, SentMessage
from rest_framework import serializers


class ReceivedMessageSerializer(serializers.ModelSerializer):
    class Meta:
        model = ReceivedMessage
        fields = '__all__'


class SentMessageSerializer(serializers.ModelSerializer):
    class Meta:
        model = SentMessage
        fields = '__all__'
