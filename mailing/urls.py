from django.urls import path

from mailing.apps import MailingConfig
from mailing.views import IndexView, MailingListView, MailingCreateView, MailingDeleteView, MailingUpdateView, \
    MailingDetailView, LogDetailView, LogListView, AccessErrorView

app_name = MailingConfig.name

urlpatterns = [
    path('', IndexView.as_view(), name='index'),
    path('mailing_list/', MailingListView.as_view(), name='mailing_list'),
    path('mailing_create/', MailingCreateView.as_view(), name='mailing_create'),
    path('mailing_update/<slug:slug>/', MailingUpdateView.as_view(), name='mailing_update'),
    path('mailing_delete/<slug:slug>/', MailingDeleteView.as_view(), name='mailing_delete'),
    path('mailing_detail/<slug:slug>/', MailingDetailView.as_view(), name='mailing_detail'),
    path('log_list/', LogListView.as_view(), name='log_list'),
    path('log_view/<int:pk>/', LogDetailView.as_view(), name='log_detail'),
    path('403error/', AccessErrorView.as_view(), name='access_error'),
]
