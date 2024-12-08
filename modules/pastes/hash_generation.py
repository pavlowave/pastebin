"""
Генерация и декодирование хеша
"""

from base64 import b64decode, b64encode


def hash_encode(message_id: str) -> str:
    """
    Кодирование message id
    :param message_id: message id
    """
    message_id_bytes = message_id.encode("utf-8")
    base64_bytes = b64encode(message_id_bytes)
    base64_message_id = base64_bytes.decode("utf-8")
    return base64_message_id


def hash_decode(message_hash: str) -> str:
    """
    Декодирование message id
    :param message_hash: хэш message id
    """
    base64_bytes = message_hash.encode("utf-8")
    message_bytes = b64decode(base64_bytes)
    message_id = message_bytes.decode("utf-8")
    return message_id