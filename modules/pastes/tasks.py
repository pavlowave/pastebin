"""
Настройка задачи для Celery
"""

from django.utils import timezone

from drive.message import GDrive
from pastebin.celery import app

from .hash_generation import hash_decode
from .models import Text


@app.task(name="delete_message_drive")
def delete_message_drive() -> None:
    """
    Удаление временных сообщений, срок действия которых истек
    """
    current_date = timezone.now()
    irrelevant_messages = Text.objects.filter(
        datetime_of_deletion__lte=current_date
    )
    for message_id in irrelevant_messages.values_list("drive_id", flat=True):
        decoded_hash = hash_decode(message_id)
        GDrive.delete(decoded_hash)
    irrelevant_messages.delete()