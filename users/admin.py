from django.contrib import admin

from users.models import User


@admin.action(description="Блокировать пользователя сервиса")
def make_status(self, request, queryset):
    queryset.update(is_active=False)


class UserAdmin(admin.ModelAdmin):
    list_display = ('id', 'email', 'is_active', 'phone',)
    actions = [make_status]


admin.site.register(User, UserAdmin)
