import boto3
from botocore.exceptions import ClientError
from django.conf import settings

class YandexS3Client:
    def __init__(self):
        self.s3 = boto3.client(
            's3',
            aws_access_key_id=settings.AWS_ACCESS_KEY_ID,
            aws_secret_access_key=settings.AWS_SECRET_ACCESS_KEY,
            endpoint_url=settings.AWS_S3_ENDPOINT_URL,
            region_name=settings.AWS_S3_REGION_NAME,
        )
        self.bucket_name = settings.AWS_STORAGE_BUCKET_NAME

    def upload_file(self, file_path: str):
        object_name = file_path.split("/")[-1]  # Извлекаем имя файла
        try:
            with open(file_path, "rb") as file:
                self.s3.put_object(
                    Bucket=self.bucket_name,
                    Key=object_name,
                    Body=file,
                )
            print(f"File {object_name} uploaded to {self.bucket_name}")
        except ClientError as e:
            print(f"Error uploading file: {e}")

    def delete_file(self, object_name: str):
        try:
            self.s3.delete_object(Bucket=self.bucket_name, Key=object_name)
            print(f"File {object_name} deleted from {self.bucket_name}")
        except ClientError as e:
            print(f"Error deleting file: {e}")

    def get_file(self, object_name: str, destination_path: str):
        try:
            response = self.s3.get_object(Bucket=self.bucket_name, Key=object_name)
            data = response['Body'].read()
            with open(destination_path, "wb") as file:
                file.write(data)
            print(f"File {object_name} downloaded to {destination_path}")
        except ClientError as e:
            print(f"Error downloading file: {e}")
