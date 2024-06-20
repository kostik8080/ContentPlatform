from django.contrib.auth.models import AbstractUser
from django.db import models

NULLABLE = {'null': True, 'blank': True}


class Subscription(models.Model):
    payment_date = models.DateField(verbose_name='Дата оплаты', **NULLABLE)
    payment_session = models.CharField(max_length=400, verbose_name='Сессия по оплате', **NULLABLE)
    payment_url = models.URLField(verbose_name='Ссылка на оплату',  **NULLABLE, max_length=500)


class User(AbstractUser):
    username = None
    phone = models.CharField(max_length=20, unique=True, verbose_name='Номер телефона')
    email = models.EmailField(unique=True, verbose_name='Почта')
    first_name = models.CharField(max_length=30, verbose_name='Имя')
    last_name = models.CharField(max_length=30, verbose_name='Фамилия')
    city = models.CharField(max_length=100, verbose_name='Город', **NULLABLE)
    avatar = models.ImageField(upload_to='avatars', **NULLABLE)
    post_count = models.IntegerField(default=0)

    is_subscribed = models.OneToOneField(to=Subscription, on_delete=models.CASCADE,
                                         verbose_name='Подписка',  **NULLABLE)

    USERNAME_FIELD = 'phone'
    REQUIRED_FIELDS = ['email']
