from django.forms import forms

from customers.models import Customer
from users.forms import StyleFormMixin


class CustomerForm(StyleFormMixin, forms.ModelForm):
    """Форма для создания/редактирования клиента сервиса"""
    class Meta:
        model = Customer
        exclude = ('created_by',)