from django.contrib.auth.mixins import PermissionRequiredMixin, LoginRequiredMixin
from django.shortcuts import redirect
from django.urls import reverse_lazy
from django.utils.text import slugify
from django.views.generic import ListView, CreateView, UpdateView, DeleteView, DetailView

from customers.forms import CustomerForm
from customers.models import Customer


class CustomerListView(ListView):
    """Контроллер просмотра всех рассылок"""
    model = Customer
    paginate_by = 15  # количество элементов на одну страницу
    ordering = ['-id']

    def dispatch(self, request, *args, **kwargs):  # запрет доступа без авторизации
        if self.request.user.is_anonymous:
            return redirect('mailing:access_error')
        return super().dispatch(request, *args, **kwargs)

    # def get_queryset(self, *args, **kwargs):  # отображение только тех контактов, которые созданы пользователем
    #     queryset = super().get_queryset()
    #     # if not self.request.user.is_manager:  # менеджеру доступны все контакты
    #     #     queryset = queryset.filter(created_by=self.request.user.slug)
    #     return queryset


class CustomerCreateView(LoginRequiredMixin, CreateView):
    """Контроллер создания рассылки"""
    model = Customer
    form_class = CustomerForm
    success_url = reverse_lazy('customers:customer_list')

    def form_valid(self, form):  # автоматическое присвоение автора
        if form.is_valid():
            contact = form.save()
            contact.created_by = self.request.user
            contact.slug = slugify(contact.first_name)  # Автоматическое заполнение slug по имени
            contact.save()

        return super().form_valid(form)

    def dispatch(self, request, *args, **kwargs):  # запрет доступа без авторизации
        if self.request.user.is_anonymous:
            return redirect('mailing:access_error')
        return super().dispatch(request, *args, **kwargs)


class CustomerUpdateView(UpdateView):
    """Контроллер редактирования рассылки"""
    model = Customer
    fields = '__all__'
    success_url = reverse_lazy('customers:customer_list')


class CustomerDeleteView(DeleteView):
    """Контроллер удаления рассылки"""
    model = Customer
    success_url = reverse_lazy('customers:customer_list')


class CustomerDetailView(DetailView):
    """Контроллер просмотра деталей рассылки"""
    model = Customer
