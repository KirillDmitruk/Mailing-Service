from django.db import models

NULLABLE = {'blank': True, 'null': True}


class Customer(models.Model):
    email = models.EmailField(verbose_name='email')
    first_name = models.CharField(max_length=50, verbose_name='first name')
    last_name = models.CharField(max_length=50, verbose_name='last name')
    middle_name = models.CharField(max_length=50, verbose_name='middle name')
    comment = models.TextField(verbose_name='comment')
    slug = models.CharField(max_length=150, **NULLABLE, verbose_name='URL', unique=True)
    created_by = models.ForeignKey('users.User', on_delete=models.CASCADE, null=True, blank=True, verbose_name='автор')

    def __str__(self):
        return f'{self.last_name} {self.first_name}: {self.email}'

    class Meta:
        verbose_name = 'customer'
        verbose_name_plural = 'customers'
