from django import forms
from django.contrib.auth.forms import UserCreationForm, UserChangeForm

from users.models import User


class StyleFormMixin:
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field_name, field in self.fields.items():
            field.widget.attrs['class'] = 'form-control'


class UserProfileForm(UserChangeForm):
    """Изменение профиля"""
    class Meta:
        model = User
        fields = ('email', 'first_name', 'last_name', 'phone',)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['password'].widget = forms.HiddenInput()


class UserRegisterForm(StyleFormMixin, UserCreationForm):
    """Форма регистрации"""

    class Meta:
        model = User
        fields = ('email', 'password1', 'password2')


class CustomPasswordResetForm(forms.Form):
    """Форма для сброса пароля"""
    email = forms.EmailField(
        label="email", max_length=254, help_text="Введите email для отправки"
    )


class UserStatusForm(UserChangeForm):
    """Форма для управления статусом пользователя"""
    class Meta:
        model = User
        fields = ('is_active',)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['password'].widget = forms.HiddenInput()
