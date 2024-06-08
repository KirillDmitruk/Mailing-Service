from django.contrib import admin

from customers.models import Customer


@admin.register(Customer)
class CustomerAdmin(admin.ModelAdmin):
    list_display = ('id', 'email', 'first_name', 'last_name', 'comment',)
    search_fields = ('email', 'first_name', 'last_name',)
