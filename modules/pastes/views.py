import os
import base64
from datetime import timedelta
from django.http import JsonResponse, Http404
from django.shortcuts import get_object_or_404
from .models import Paste
from django.utils.timezone import now
import boto3

# Функция для генерации случайной строки в base64
def get_random_base64_string(length=8):
    random_bytes = os.urandom(length)
    base64_string = base64.urlsafe_b64encode(random_bytes).decode('utf-8')
    return base64_string[:length]  # Ограничиваем длину строки

def create_paste(request):
    content = request.POST.get('content')
    expires_in = int(request.POST.get('expires_in', 3600))  # Время жизни пасты в секундах

    # Сохраняем текст в Yandex Cloud Object Storage
    s3 = boto3.client('s3', endpoint_url='https://storage.yandexcloud.net')
    bucket_name = 'название_вашего_бакета'
    key = get_random_base64_string(8)  # Генерация уникального ключа для файла в base64
    s3.put_object(Bucket=bucket_name, Key=key, Body=content.encode('utf-8'))

    # Создаём метаданные
    expires_at = now() + timedelta(seconds=expires_in)
    paste = Paste.objects.create(content_url=f'https://{bucket_name}.storage.yandexcloud.net/{key}', expires_at=expires_at)

    return JsonResponse({'slug': paste.slug}, status=201)

def get_paste(request, slug):
    paste = get_object_or_404(Paste, slug=slug)
    if paste.is_expired():
        paste.delete()
        raise Http404("Paste has expired")

    content = paste.get_content()
    return JsonResponse({'content': content})
