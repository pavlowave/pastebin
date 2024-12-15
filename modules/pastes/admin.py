"""
Регистрация и настройка моделей для админ-панели
"""

# from django.contrib import admin

# from text.models import Text


# @admin.register(Text)
# class MessageAdmin(admin.ModelAdmin):
#     list_display = (
#         "pk",
#         "author",
#         "is_temporary",
#         "is_private",
#         "datetime_of_deletion",
#     )
#     list_display_links = ("pk", "author")
#     list_filter = ("is_temporary", "is_private", "author")
#     list_per_page = 15
#     ordering = ("pk", "datetime_of_deletion")
#     search_fields = ("author__username",)