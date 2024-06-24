from django.db import IntegrityError
from django.shortcuts import redirect
from django.urls import reverse_lazy
from django.utils.text import slugify
from django.views.generic import ListView, CreateView, UpdateView, DeleteView, DetailView, TemplateView

from mailing.views import OwnerRequiredMixin
from message.forms import MessageForm
from message.models import Message


class MessageListView(ListView):
    """Контроллер просмотра всех рассылок"""
    model = Message
    paginate_by = 6  # количество элементов на одну страницу
    ordering = ['-id']

    def dispatch(self, request, *args, **kwargs):  # запрет доступа без авторизации
        if self.request.user.is_anonymous:
            return redirect('mailing:access_error')
        return super().dispatch(request, *args, **kwargs)

    # def get_queryset(self, *args, **kwargs):  # отображение только тех сообщений, которые созданы пользователем
    #     queryset = super().get_queryset()
    #     if not self.request.user.is_manager:  # менеджеру доступны все сообщения
    #         queryset = queryset.filter(created_by=self.request.user.pk)
    #     return queryset


class MessageCreateView(CreateView):
    """Контроллер создания рассылки"""
    model = Message
    form_class = MessageForm
    success_url = reverse_lazy('message:message_list')

    def form_valid(self, form):  # автоматическое присвоение автора
        if form.is_valid():
            product = form.save()
            product.created_by = self.request.user
            product.slug = slugify(product.topic) + str(product.id)  # Автоматическое заполнение slug по теме
            product.save()
        return super().form_valid(form)


class MessageUpdateView(OwnerRequiredMixin, UpdateView):
    """Контроллер редактирования рассылки"""
    model = Message
    form_class = MessageForm
    success_url = reverse_lazy('message:message_list')


class MessageDeleteView(OwnerRequiredMixin, DeleteView):
    """Контроллер удаления рассылки"""
    model = Message
    success_url = reverse_lazy('message:message_list')


class MessageDetailView(DetailView):
    """Контроллер просмотра деталей """
    model = Message


class NotUniqueView(TemplateView):
    """Контроллер ошибки доступа"""
    template_name = 'message/not_unique.html'
