# Generated by Django 4.2 on 2024-06-13 18:52

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('menenger', '0004_content_count_views'),
    ]

    operations = [
        migrations.AddField(
            model_name='content',
            name='likes',
            field=models.IntegerField(blank=True, default=0, null=True, verbose_name='Количество лайков'),
        ),
    ]
