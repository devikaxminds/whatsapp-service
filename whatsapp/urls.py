from django.urls import path
from .views import SendMessageView, WebhookView

urlpatterns = [
    path("send-message/", SendMessageView.as_view(), name="send-message"),
    path("webhook/", WebhookView.as_view(), name="webhook"),
]
