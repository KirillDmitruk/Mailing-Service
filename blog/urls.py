from django.urls import path
from django.views.decorators.cache import cache_page

from blog.apps import BlogConfig
from blog.views import ArticleListView, ArticleDetailView

app_name = BlogConfig.name

urlpatterns = [
    path('article_list/', cache_page(60)(ArticleListView.as_view()), name='article_list'),
    path('article_view/<int:pk>/', cache_page(60)(ArticleDetailView.as_view()), name='article_detail'),
]
