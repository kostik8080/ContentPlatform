# Generated by Django 4.2 on 2024-06-12 15:36

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Content',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=100, verbose_name='Название')),
                ('content', models.TextField(verbose_name='Контент')),
                ('photo', models.ImageField(upload_to='content/', verbose_name='Фотография')),
                ('published', models.BooleanField(default=False, verbose_name='Опубликовано')),
                ('created', models.DateTimeField(auto_now_add=True, verbose_name='Дата создания')),
                ('updated', models.DateTimeField(auto_now=True, verbose_name='Дата обновления')),
            ],
            options={
                'verbose_name': 'Контент',
                'verbose_name_plural': 'Контенты',
                'ordering': ['-title', '-created'],
            },
        ),
    ]
