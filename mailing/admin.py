from django.contrib import admin

from mailing.models import Mailing


@admin.register(Mailing)
class MailingAdmin(admin.ModelAdmin):
    list_display = ('id', 'topic_mailing', 'message', 'datetime_start', 'datetime_finish', 'period', 'status',)
    list_filter = ('period', 'status',)
    search_fields = ('id', 'period', 'status', 'clients',)
