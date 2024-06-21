from django.db import models

from users.models import User

NULLABLE = {'null': True, 'blank': True}


class Content(models.Model):
    title = models.CharField(max_length=100, verbose_name='Название')
    content = models.TextField(verbose_name='Контент')
    photo = models.ImageField(verbose_name='Фотография', upload_to='content/', **NULLABLE)
    published = models.BooleanField(default=False, verbose_name='Опубликовано')
    is_paid = models.BooleanField(default=False, verbose_name='Оплачено')
    count_views = models.IntegerField(default=0, verbose_name='Количество просмотров', **NULLABLE)
    created = models.DateTimeField(auto_now_add=True, verbose_name='Дата создания')
    updated = models.DateTimeField(auto_now=True, verbose_name='Дата обновления')

    author = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name='Автор', **NULLABLE)

    class Meta:
        verbose_name = 'Контент'
        verbose_name_plural = 'Контенты'
        ordering = ['-title', '-created']

    def __str__(self):
        return self.title


class Like(models.Model):

    user = models.ForeignKey(User, on_delete=models.CASCADE)
    content = models.ForeignKey(Content, on_delete=models.CASCADE)
    like = models.BooleanField(default=False, verbose_name='Лайк/Дизлайк')

    class Meta:
        verbose_name = 'Лайк'
        verbose_name_plural = 'Лайки'

    def __str__(self):
        return f'{self.user.first_name} {self.user.last_name}: {self.content.title}'
