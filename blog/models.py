from django.db import models


class Article(models.Model):
    """Статья"""
    title = models.CharField(max_length=100, verbose_name='заголовок')
    body = models.TextField(verbose_name='содержимое')
    preview = models.ImageField(upload_to='articles/', null=True, blank=True, verbose_name='изображение')
    date = models.DateField(verbose_name='дата публикации')
    views_count = models.PositiveIntegerField(default=0, verbose_name='просмотры')

    def __str__(self):
        return f'{self.title}'

    class Meta:
        verbose_name = 'статья'
        verbose_name_plural = 'статьи'
