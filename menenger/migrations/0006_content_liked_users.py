# Generated by Django 4.2 on 2024-06-13 19:07

from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('menenger', '0005_content_likes'),
    ]

    operations = [
        migrations.AddField(
            model_name='content',
            name='liked_users',
            field=models.ManyToManyField(related_name='liked_content', to=settings.AUTH_USER_MODEL),
        ),
    ]
