import random
import secrets  # 5
import string

from django.core.mail import send_mail
from django.shortcuts import get_object_or_404, redirect, render
from django.urls import reverse_lazy, reverse
from django.views.generic import CreateView, FormView, UpdateView, ListView

from config.settings import EMAIL_HOST_USER
from mailing.views import ManagerRequiredMixin
from users.forms import UserRegisterForm, UserProfileForm, UserStatusForm
from users.models import User


class RegisterUser(CreateView):
    """Контроллер для верификации"""
    model = User
    form_class = UserRegisterForm
    success_url = reverse_lazy('users:login')

    def form_valid(self, form):  # 2
        user = form.save()
        user.is_active = False  # 3
        token = secrets.token_hex(16)  # 6
        user.token = token
        user.save()
        host = self.request.get_host()
        url = f'http://{host}/users/email-confirm/{token}/'  # 7
        send_mail(
            subject='Подтверждение регистрации',
            message=f'Здравствуйте! Для подтверждения регистрации перейдите по ссылке: {url}',
            from_email=EMAIL_HOST_USER,
            recipient_list=[user.email],
        )  # 8
        return super().form_valid(form)  # 9


def email_verification(request, token):
    user = get_object_or_404(User, token=token)
    user.is_active = True
    user.save()
    return redirect(reverse('users:login'))  # 10


def check_email(request):
    return render(request, 'users/check_email.html')


class ProfileView(UpdateView):
    model = User
    form_class = UserProfileForm
    success_url = reverse_lazy('mailing:index')

    def get_object(self, queryset=None):
        return self.request.user


class PasswordResetView(FormView):
    """Контроллер для воостановления пароля"""
    template_name = "users/password_reset.html"
    success_url = reverse_lazy("users:login")

    def form_valid(self, form):
        email_form = form.cleaned_data["email"]
        try:
            user = User.objects.get(email=email_form)
        except User.DoesNotExist:
            return render(self.request, self.template_name,
                          {"form": form, "error": "Пользователь с таким email-ом не найден."})

        new_password = ''.join(random.choices(string.ascii_letters + string.digits, k=8))
        user.set_password(new_password)
        user.save()

        send_mail(
            subject="Новый пароль",
            message=f"Ваш новый пароль: {new_password}",
            from_email=EMAIL_HOST_USER,
            recipient_list=[user.email],
            fail_silently=False,
        )

        return super().form_valid(form)


class UserUpdateView(ManagerRequiredMixin, UpdateView):
    """Контроллер редактирования пользователя"""
    model = User
    form_class = UserStatusForm
    success_url = reverse_lazy('users:user_list')


class UserListView(ListView):
    """Контроллер просмотра списка пользователей"""
    model = User
    paginate_by = 9  # количество элементов на одну страницу
    ordering = ['-id']

    def dispatch(self, request, *args, **kwargs):  # отображение списка только для менеджера
        if self.request.user.is_anonymous:
            return redirect('mailing:access_error')
        # elif not self.request.user.is_manager:
        #     return redirect('mailing:access_error')
        return super().dispatch(request, *args, **kwargs)
