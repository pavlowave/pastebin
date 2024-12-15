"""
Cериализатор
"""

from rest_framework import serializers
from .models import TextLink

class TextLinkSerializer(serializers.ModelSerializer):
    class Meta:
        model = TextLink
        fields = ['text', 's3_url']



# from rest_framework import serializers
# from django.core.exceptions import ValidationError
# from django.utils import timezone
# from django_recaptcha.fields import ReCaptchaField
# from django_recaptcha.widgets import ReCaptchaV2Checkbox

# class InputTextSerializer(serializers.Serializer):
#     message = serializers.CharField(
#         label="Сообщение",
#         required=True,
#         style={"base_template": "textarea.html"},
#     )
#     is_temporary = serializers.BooleanField(
#         label="Временное сообщение",
#         required=False,
#         default=False,
#     )
#     is_private = serializers.BooleanField(
#         label="Приватное сообщение (доступно только по ссылке)",
#         required=False,
#         default=False,
#     )
#     datetime_of_deletion = serializers.DateTimeField(
#         label="Дата и время уничтожения сообщения*",
#         required=False,
#         input_formats=["%Y-%m-%dT%H:%M"],
#     )
#     captcha = serializers.CharField(write_only=True)  # Для капчи будет передаваться строка

#     def validate_datetime_of_deletion(self, value):
#         if value is not None and timezone.now() >= value:
#             raise ValidationError(
#                 "Дата и время уничтожения сообщения не могут быть меньше текущих"
#             )
#         return value

#     def validate(self, data):
#         # Валидация для captcha
#         captcha_response = data.get("captcha")
#         if not self.validate_captcha(captcha_response):
#             raise ValidationError("Неверная капча")
#         return data

#     def validate_captcha(self, captcha_response):
#         # Здесь нужно подключить логику валидации капчи через API
#         # Пример для reCAPTCHA v2, или использовать готовую библиотеку для DRF
#         # Это простой пример для валидации:
#         # Для реальной валидации нужно интегрировать с сервисом reCAPTCHA.
#         return True  # Заглушка: замените на реальную логику проверки
