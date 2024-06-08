from django.db import models

NULLABLE = {'blank': True, 'null': True}


class Message(models.Model):
    topic = models.CharField(max_length=100, verbose_name='topic')
    text = models.TextField(verbose_name='text')
    slug = models.CharField(max_length=150, **NULLABLE, verbose_name='URL')
    created_by = models.ForeignKey('users.User', on_delete=models.CASCADE, null=True, blank=True, verbose_name='автор')

    def __str__(self):
        return self.topic

    class Meta:
        verbose_name = 'message'
        verbose_name_plural = 'messages'
