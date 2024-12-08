"""
Конфигурация URL-адресов сообщений
"""

from django.urls import path

from text.views import (
    DeleteMessageDoneView,
    DeleteMessageView,
    InputTextView,
    MessageFeedView,
    ShowMessageView,
    UserMessageFeedView,
)

urlpatterns = [
    path(
        "",
        InputTextView.as_view(),
        name="input_text"
    ),
    path(
        "message/<uuid:uuid_url>/",
        ShowMessageView.as_view(),
        name="show_message",
    ),
    path(
        "message-feed/",
        MessageFeedView.as_view(),
        name="message_feed"
    ),
    path(
        "my-messages/",
        UserMessageFeedView.as_view(),
        name="user_message_feed"
    ),
    path(
        "delete-message/<uuid:uuid_url>/",
        DeleteMessageView.as_view(),
        name="delete_message",
    ),
    path(
        "delete-message/done/",
        DeleteMessageDoneView.as_view(),
        name="delete_message_done",
    ),
]