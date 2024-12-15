import boto3
from django.conf import settings

class S3Service:
    def __init__(self):
        """Инициализация клиента S3"""
        self.client = boto3.client(
            service_name='s3',
            endpoint_url=settings.AWS_S3_ENDPOINT_URL,
            aws_access_key_id=settings.AWS_ACCESS_KEY_ID,
            aws_secret_access_key=settings.AWS_SECRET_ACCESS_KEY,
        )

    def create_bucket(self, bucket_name):
        """Создать бакет"""
        self.client.create_bucket(Bucket=bucket_name)

    def upload_file(self, file_obj, bucket_name, key):
        """Загрузить файл в бакет"""
        self.client.upload_fileobj(file_obj, bucket_name, key)

    def list_objects(self, bucket_name):
        """Получить список объектов в бакете"""
        response = self.client.list_objects(Bucket=bucket_name)
        return [obj['Key'] for obj in response.get('Contents', [])]

    def delete_objects(self, bucket_name, keys):
        """Удалить объекты из бакета"""
        delete_format = [{'Key': key} for key in keys]
        self.client.delete_objects(Bucket=bucket_name, Delete={'Objects': delete_format})

    def get_object(self, bucket_name, key):
        """Скачать объект из бакета"""
        response = self.client.get_object(Bucket=bucket_name, Key=key)
        return response['Body'].read()
    def upload_text(self, text, bucket_name, key):
        """Метод для загрузки текста в S3"""
        try:
            # Загружаем текст как объект в S3
            self.client.put_object(Bucket=bucket_name, Key=key, Body=text, StorageClass='COLD')
        except Exception as e:
            raise Exception(f"Failed to upload text to S3: {str(e)}")