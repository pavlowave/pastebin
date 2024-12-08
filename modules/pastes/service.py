"""
Функции для взаимодействия с моделями
"""

import uuid
from django.contrib.auth import get_user_model
from drive.message import GDrive
from text.forms import InputTextForm
from text.hash_generation import hash_encode
from text.models import Text

User = get_user_model()


def create_message(form: InputTextForm, uuid_url: uuid, author: User) -> None:
    """
    Создание сообщения
    :param form: заполненная форма
    :param uuid_url: уникальный URL-адрес сообщения
    :paramauthor: автор сообщения
    """

    message = form.cleaned_data["message"]
    message_name = f"{uuid_url}.txt"
    with open(message_name, "w") as file:
        file.write(message)
    message_id = GDrive.upload(message_name)
    encoded_message_id = hash_encode(message_id)

    Text.objects.create(
        uuid_url=uuid_url,
        drive_id=encoded_message_id,
        is_temporary=form.cleaned_data["is_temporary"],
        datetime_of_deletion=form.cleaned_data["datetime_of_deletion"],
        is_private=form.cleaned_data["is_private"],
        author=author,
    )