"""
Настройка моделей для базы данных
"""

from django.db import models

class TextLink(models.Model):
    text = models.TextField()
    s3_key = models.CharField(max_length=255, unique=True)
    s3_url = models.URLField()

    def __str__(self):
        return f"Text {self.s3_key} - URL {self.s3_url}"



# from django.contrib.auth import get_user_model
# from django.db import models

# User = get_user_model()


# class Text(models.Model):
#     """Сообщение"""

#     uuid_url = models.UUIDField(unique=True, editable=False)
#     drive_id = models.CharField(max_length=44, verbose_name="Хэш id файла")
#     is_temporary = models.BooleanField(
#         default=False,
#         verbose_name="Сообщение временное"
#     )
#     datetime_of_deletion = models.DateTimeField(
#         blank=True,
#         null=True,
#         verbose_name="Дата удаления"
#     )
#     author = models.ForeignKey(
#         User,
#         on_delete=models.CASCADE,
#         related_name="author",
#         blank=True,
#         null=True,
#         verbose_name="Автор",
#     )
#     datetime_of_creation = models.DateTimeField(
#         auto_now_add=True,
#         verbose_name="Дата создания"
#     )
#     is_private = models.BooleanField(default=False, verbose_name="Приватное")

#     def __str__(self):
#         if self.author is not None:
#             return f"Сообщение от {self.author.username}"
#         else:
#             return "Анонимное сообщение"

#     class Meta:
#         ordering = ("-pk",)
#         verbose_name = "Сообщение"
#         verbose_name_plural = "Сообщения"