from django.db import models

from customers.models import Customer
from message.models import Message
from users.models import User

NULLABLE = {'blank': True, 'null': True}


class Mailing(models.Model):
    """Рассылка"""

    """варианты периодичности рассылки"""
    ONCE = 'Единоразовая'
    DAILY = 'Раз в день'
    WEEKLY = 'Раз в неделю'
    MONTHLY = 'Раз в месяц'

    PERIOD_CHOICES = (
        (ONCE, 'Единоразовая'),
        (DAILY, 'Раз в день'),
        (WEEKLY, 'Раз в неделю'),
        (MONTHLY, 'Раз в месяц'),
    )

    """варианты статуса рассылки"""
    CREATED = 'created'
    STARTED = 'started'
    FINISHED = 'finished'

    STATUS_CHOICES = (
        (CREATED, 'Создана'),
        (STARTED, 'Запущена'),
        (FINISHED, 'Завершена'),
    )

    topic_mailing = models.CharField(max_length=150, unique=True, null=True, blank=True, verbose_name='название рассылки')
    message = models.ForeignKey(Message, on_delete=models.CASCADE, verbose_name='message')
    clients = models.ManyToManyField(Customer, verbose_name='контакты клиентов')
    datetime_start = models.DateTimeField(verbose_name='время начала рассылки')
    datetime_finish = models.DateTimeField(verbose_name='время окончания рассылки')
    period = models.CharField(max_length=25, choices=PERIOD_CHOICES, default=DAILY, verbose_name='period')
    status = models.CharField(max_length=25, choices=STATUS_CHOICES, default=CREATED, verbose_name='status')
    slug = models.CharField(max_length=150, **NULLABLE, verbose_name='URL')
    created_by = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True, verbose_name='автор')

    def __str__(self):
        return f'{self.datetime_start}-{self.datetime_finish}, {self.period}, {self.status}'

    class Meta:
        verbose_name = 'mailing'
        verbose_name_plural = 'mailing'


class Log(models.Model):
    """Логи рассылки"""
    SUCCESS = 'success'
    FAIL = 'fail'

    STATUSES = (
        (SUCCESS, 'успешно'),
        (FAIL, 'не успешно')
    )
    mailing = models.ForeignKey(Mailing, on_delete=models.CASCADE, verbose_name='рассылка')
    clients = models.ForeignKey(Customer, on_delete=models.CASCADE, **NULLABLE, verbose_name='контакты клиентов')
    try_time = models.DateTimeField(auto_now_add=True, verbose_name='дата и время последней попытки')
    try_status = models.CharField(max_length=50, choices=STATUSES, verbose_name='статус попытки')
    server_answer = models.CharField(max_length=250, **NULLABLE, verbose_name='ответ почтового сервера')

    def __str__(self):
        return f'{self.try_time}: {self.try_status}'

    class Meta:
        verbose_name = 'лог'
        verbose_name_plural = 'логи'