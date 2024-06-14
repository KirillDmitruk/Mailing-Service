import random

from django.shortcuts import redirect
from django.urls import reverse_lazy
from django.utils.text import slugify
from django.views.generic import ListView, CreateView, TemplateView, DeleteView, UpdateView, DetailView

from customers.models import Customer
from mailing.forms import MailingForm, MailingManagerForm
from mailing.models import Mailing, Log
from mailing.services import get_cashed_article_list


class IndexView(TemplateView):
    """Контроллер просмотра домашней страницы"""
    template_name = 'mailing/index.html'

    def get_context_data(self, **kwargs):
        context_data = super().get_context_data(**kwargs)

        article_list = list(get_cashed_article_list())
        if len(article_list) >= 3:
            article_random_list = random.sample(article_list, 3)
            context_data['article_list'] = article_random_list  # три рандомные статьи

        context_data['mailing_count'] = Mailing.objects.all().count()  # количество рассылок всего
        context_data['mailing_started_count'] = Mailing.objects.filter(status='started').count()  # активных рассылок
        context_data['mailing_clients_count'] = Customer.objects.all().count()  # уникальных клиентов

        return context_data


class OwnerRequiredMixin(DetailView):
    """Миксин проверки прав доступа к объекту, доступ только для автора"""

    def dispatch(self, request, *args, **kwargs):
        obj = self.get_object()
        if obj.created_by != request.user:
            return redirect('mailing:access_error')
        return super().dispatch(request, *args, **kwargs)


class ManagerRequiredMixin(DetailView):
    """Миксин проверки прав доступа к объекту, доступ только для менеджера"""

    def dispatch(self, request, *args, **kwargs):
        if not request.user.is_manager:
            return redirect('mailing:access_error')
        return super().dispatch(request, *args, **kwargs)


class ManagerOrOwnerRequiredMixin(DetailView):
    """Миксин проверки прав доступа к объекту, доступ только для автора и менеджера"""

    def dispatch(self, request, *args, **kwargs):
        obj = self.get_object()
        if not request.user.is_manager and obj.created_by != request.user:
            return redirect('mailing:access_error')
        return super().dispatch(request, *args, **kwargs)


class MailingListView(ListView):
    """Контроллер просмотра всех рассылок"""
    model = Mailing
    paginate_by = 9  # количество элементов на одну страницу
    ordering = ['-id']

    def get_queryset(self, *args, **kwargs):  # отображение только тех рассылок, которые созданы пользователем
        queryset = super().get_queryset()
        if not self.request.user.is_manager:  # менеджеру доступны все рассылки
            queryset = queryset.filter(created_by=self.request.user.pk)
        return queryset


class MailingCreateView(CreateView):
    """Контроллер создания рассылки"""
    model = Mailing
    form_class = MailingForm
    success_url = reverse_lazy('mailing:mailing_list')

    def get_form(self, form_class=None):  # отображение только тех контактов, которые созданы пользователем
        form = super().get_form(form_class=None)
        form.fields['clients'].queryset = form.fields['clients'].queryset.filter(created_by=self.request.user.id)
        return form

    def form_valid(self, form):  # автоматическое присвоение автора рассылки
        if form.is_valid():
            product = form.save()
            product.created_by = self.request.user
            product.slug = slugify(product.topic_mailing)  # Автоматическое заполнение slug по названию рассылки
            product.save()

        return super().form_valid(form)


class MailingUpdateView(UpdateView):
    """Контроллер редактирования рассылки"""
    model = Mailing
    form_class = MailingForm
    success_url = reverse_lazy('mailing:mailing_list')

    def get_form(self, form_class=None):  # форма редактирования рассылки для менеджера, можно изменять только статус
        if form_class is None:
            form_class = self.get_form_class()

        if self.request.user.is_manager:
            return MailingManagerForm(**self.get_form_kwargs())

        return super().get_form(form_class)


class MailingDeleteView(DeleteView):
    """Контроллер удаления рассылки"""
    model = Mailing
    success_url = reverse_lazy('mailing:mailing_list')


class MailingDetailView(DetailView):
    """Контроллер просмотра деталей рассылки"""
    model = Mailing


class LogListView(ListView):
    """Контроллер просмотра логов"""
    model = Log
    paginate_by = 9  # количество элементов на одну страницу

    def dispatch(self, request, *args, **kwargs):  # запрет доступа без авторизации
        if self.request.user.is_anonymous:
            return redirect('mailing:access_error')
        return super().dispatch(request, *args, **kwargs)

    def get_context_data(self, *args, **kwargs):  # отображение логов только тех рассылок, которые созданы пользователем
        context_data = super().get_context_data(**kwargs)
        obj_lst = []
        for log in Log.objects.all():
            if log.mailing.created_by == self.request.user or self.request.user.is_manager:  # менеджеру доступны все логи
                obj_lst.append(log)
        obj_lst.reverse()
        context_data['object_list'] = obj_lst
        return context_data


class LogDetailView(DetailView):
    """Контроллер просмотра отдельного лога"""
    model = Log

    def dispatch(self, request, *args, **kwargs):  # доступ к логу только по рассылке, которая создана пользователем
        obj = self.get_object()
        if (obj.mailing.created_by != request.user) and (not self.request.user.is_manager):  # менеджеру доступны все логи
            return redirect('mailing:access_error')
        return super().dispatch(request, *args, **kwargs)


class AccessErrorView(TemplateView):
    """Контроллер ошибки доступа"""
    template_name = 'mailing/access_error.html'
