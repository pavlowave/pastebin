"""
Скачивание, загрузка и удаление сообщений с Yandex Cloud
"""

import boto3
import os
from io import BytesIO


class YandexS3:
    ENDPOINT_URL = "https://storage.yandexcloud.net"
    ACCESS_KEY = os.environ.get("YANDEX_S3_ACCESS_KEY")
    SECRET_KEY = os.environ.get("YANDEX_S3_SECRET_KEY")
    BUCKET_NAME = os.environ.get("YANDEX_S3_BUCKET")

    S3 = boto3.client(
        "s3",
        endpoint_url=ENDPOINT_URL,
        aws_access_key_id=ACCESS_KEY,
        aws_secret_access_key=SECRET_KEY,
    )

    @classmethod
    def upload(cls, file_path: str, object_key: str) -> str:
        """
        Загрузка файла в Yandex Object Storage
        :param file_path: путь к файлу
        :param object_key: ключ объекта (имя файла в хранилище)
        :return: ключ загруженного объекта
        """
        cls.S3.upload_file(file_path, cls.BUCKET_NAME, object_key)
        return object_key

    @classmethod
    def download(cls, object_key: str) -> str:
        """
        Скачивание файла из Yandex Object Storage
        :param object_key: ключ объекта (имя файла в хранилище)
        :return: содержимое файла в виде строки
        """
        file_stream = BytesIO()
        cls.S3.download_fileobj(cls.BUCKET_NAME, object_key, file_stream)
        file_stream.seek(0)  # Возвращаемся в начало потока
        return file_stream.getvalue().decode("utf-8")

    @classmethod
    def delete(cls, object_key: str) -> None:
        """
        Удаление файла из Yandex Object Storage
        :param object_key: ключ объекта (имя файла в хранилище)
        """
        cls.S3.delete_object(Bucket=cls.BUCKET_NAME, Key=object_key)


# # Пример использования
# if __name__ == "__main__":
#     # Загрузка файла
#     uploaded_key = YandexS3.upload("local_file.txt", "uploaded_file.txt")
#     print(f"Файл загружен под ключом: {uploaded_key}")

#     # Скачивание файла
#     content = YandexS3.download("uploaded_file.txt")
#     print(f"Содержимое файла: {content}")

#     # Удаление файла
#     YandexS3.delete("uploaded_file.txt")
#     print("Файл удален.")
