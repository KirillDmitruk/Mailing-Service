from django.forms import ModelForm

from customers.models import Customer
from users.forms import StyleFormMixin


class CustomerForm(StyleFormMixin, ModelForm):
    """Форма для создания/редактирования клиента сервиса"""
    class Meta:
        model = Customer
        exclude = ('created_by', 'slug',)