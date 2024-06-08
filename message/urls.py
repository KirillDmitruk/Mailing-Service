from django.urls import path

from message.apps import MessageConfig

from message.views import MessageListView, MessageCreateView, MessageUpdateView, MessageDeleteView, MessageDetailView

app_name = MessageConfig.name

urlpatterns = [
    path('message_list/', MessageListView.as_view(), name='message_list'),
    path('message_create/', MessageCreateView.as_view(), name='message_create'),
    path('message_update/<slug:slug>/', MessageUpdateView.as_view(), name='message_update'),
    path('message_delete/<slug:slug>/', MessageDeleteView.as_view(), name='message_delete'),
    path('message_detail/<slug:slug>/', MessageDetailView.as_view(), name='message_detail'),
]
