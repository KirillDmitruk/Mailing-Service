from django.shortcuts import redirect
from django.views.generic import ListView, DetailView

from blog.models import Article


class ArticleListView(ListView):
    """Контроллер просмотра списка статей"""
    model = Article
    paginate_by = 6  # количество элементов на одну страницу

    def dispatch(self, request, *args, **kwargs):  # запрет доступа без авторизации
        if self.request.user.is_anonymous:
            return redirect('mailing:access_error')
        return super().dispatch(request, *args, **kwargs)


class ArticleDetailView(DetailView):
    """Контроллер просмотра отдельной статьи"""
    model = Article

    def get_object(self, queryset=None):  # счетчик просмотров
        article = super().get_object(queryset)
        article.views_count += 1
        article.save()
        return article
