from enum import verify

from django.contrib.auth.views import LoginView, LogoutView
from django.urls import path

from users.apps import UsersConfig
from users.forms import CustomPasswordResetForm
from users.views import RegisterUser, email_verification, PasswordResetView, ProfileView, check_email, UserListView, \
    UserUpdateView

app_name = UsersConfig.name

urlpatterns = [
    path('login/', LoginView.as_view(template_name='users/login.html'), name='login'),
    path('logout/', LogoutView.as_view(), name='logout'),
    path('register/', RegisterUser.as_view(), name='register'),
    path('email-confirm/<str:token>/', email_verification, name='email-confirm'),  # 11
    path('password-reset/', PasswordResetView.as_view(form_class=CustomPasswordResetForm), name="password_reset",),
    path('profile/', ProfileView.as_view(), name='profile'),
    path('verify/<int:id_user>', verify, name='verify'),
    path('check_email', check_email, name='check_email'),
    path('list/', UserListView.as_view(), name='user_list'),
    path('edit/<int:pk>/', UserUpdateView.as_view(), name='user_edit'),
]
