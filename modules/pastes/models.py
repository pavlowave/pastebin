from django.db import models
from django.utils.crypto import get_random_string
from django.utils.timezone import now
import boto3
from datetime import timedelta

class Paste(models.Model):
    content_url = models.URLField()
    slug = models.SlugField(unique=True)
    created_at = models.DateTimeField(auto_now_add=True)
    expires_at = models.DateTimeField()

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = get_random_string(8)
        super().save(*args, **kwargs)

    def is_expired(self):
        return now() > self.expires_at

    def get_content(self):
        # Получаем файл из Yandex Cloud Object Storage
        s3 = boto3.client('s3', endpoint_url='https://storage.yandexcloud.net')
        bucket_name = 'название_вашего_бакета'
        key = self.content_url.split('/')[-1]  # Извлекаем ключ из URL
        return s3.get_object(Bucket=bucket_name, Key=key)['Body'].read().decode('utf-8')
