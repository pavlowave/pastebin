"""
View сообщений
"""

import uuid
from modules.pastes.serializers import TextLinkSerializer
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.conf import settings
from modules.cloud_storage.yandex_s3_client import S3Service
from .models import TextLink
from rest_framework.exceptions import ValidationError
from django.shortcuts import render, get_object_or_404

s3_service = S3Service()


class CreateText(APIView):
    def post(self, request):
        """Получить текст и сохранить его в S3"""
        text = request.data.get('text')
        if not text:
            raise ValidationError({"error": "Требуется текст"})

        key = f"texts/{uuid.uuid4().hex}.txt"

        try:
            s3_service.upload_text(text, settings.S3_BUCKET_NAME, key)
        except Exception as e:
            return Response({"error": f"Не удалось загрузить текст в S3.: {str(e)}"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

        text_link = TextLink.objects.create(
            text=text,
            s3_key=key,
            s3_url=f"{settings.S3_ENDPOINT_URL}/{settings.S3_BUCKET_NAME}/{key}"
        )

        serializer = TextLinkSerializer(text_link)

        return Response(serializer.data, status=status.HTTP_201_CREATED)


class ListText(APIView):
    def get(self, request):
        """Возвращает список всех объектов TextLink с их текстами и ссылками на S3"""
        texts = TextLink.objects.all()
        return render(request, 'index/index.html', {'texts': texts})


class DetailText(APIView):
    def get(self, request, pk):
        """Возвращает детали конкретного текста в формате HTML"""
        text_link = get_object_or_404(TextLink, pk=pk)
        return render(request, 'index/detail.html', {'text_link': text_link})
