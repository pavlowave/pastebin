"""
View сообщений
"""
import uuid

from django.shortcuts import get_object_or_404
from rest_framework import status, permissions
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from rest_framework.views import APIView

from drive.message import GDrive
from text.models import Text
from text.hash_generation import hash_decode
from text.service import create_message
from text.serializers import InputTextSerializer, TextSerializer


class InputTextAPIView(APIView):
    """Генерация сообщений"""

    def post(self, request, *args, **kwargs):
        serializer = InputTextSerializer(data=request.data)
        if serializer.is_valid():
            uuid_url = uuid.uuid4()
            author = request.user if request.user.is_authenticated else None
            create_message(serializer.validated_data, uuid_url, author)

            return Response(
                {
                    "message": "Сообщение успешно создано",
                    "uuid_url": uuid_url,
                },
                status=status.HTTP_201_CREATED,
            )
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class ShowMessageAPIView(APIView):
    """Отображение сообщения"""

    def get(self, request, uuid_url, *args, **kwargs):
        message_object = get_object_or_404(Text, uuid_url=uuid_url)
        drive_id = hash_decode(message_object.drive_id)
        content = GDrive.download(drive_id)

        serializer = TextSerializer(message_object)
        return Response(
            {
                "message": serializer.data,
                "content": content,
            },
            status=status.HTTP_200_OK,
        )


class MessageFeedAPIView(APIView):
    """Отображение ленты сообщений"""

    permission_classes = [permissions.AllowAny]

    def get(self, request, *args, **kwargs):
        messages = Text.objects.filter(is_private=False)
        serializer = TextSerializer(messages, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)


class UserMessageFeedAPIView(APIView):
    """Отображение сообщений пользователя"""

    permission_classes = [permissions.IsAuthenticated]

    def get(self, request, *args, **kwargs):
        messages = Text.objects.filter(author_id=request.user.pk)
        serializer = TextSerializer(messages, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)


class DeleteMessageAPIView(APIView):
    """Удаление сообщения"""

    permission_classes = [permissions.IsAuthenticated]

    def delete(self, request, uuid_url, *args, **kwargs):
        message = get_object_or_404(Text, uuid_url=uuid_url)

        if message.author != request.user:
            return Response({"detail": "Не авторизован"}, status=status.HTTP_403_FORBIDDEN)

        decoded_hash = hash_decode(message.drive_id)
        GDrive.delete(decoded_hash)

        message.delete()
        return Response({"detail": "Сообщение успешно удалено"}, status=status.HTTP_204_NO_CONTENT)
