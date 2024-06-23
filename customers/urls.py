from django.urls import path

from customers.apps import CustomersConfig
from customers.views import CustomerListView, CustomerCreateView, CustomerUpdateView, CustomerDeleteView, \
    CustomerDetailView, NotUniqueView

app_name = CustomersConfig.name

urlpatterns = [
    path('customer_list/', CustomerListView.as_view(), name='customer_list'),
    path('customer_create/', CustomerCreateView.as_view(), name='customer_create'),
    path('customer_update/<slug:slug>/', CustomerUpdateView.as_view(), name='customer_update'),
    path('customer_delete/<slug:slug>/', CustomerDeleteView.as_view(), name='customer_delete'),
    path('customer_detail/<slug:slug>/', CustomerDetailView.as_view(), name='customer_detail'),
    path('not_unique/', NotUniqueView.as_view(), name='not_unique'),

]
