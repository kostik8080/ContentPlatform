# Generated by Django 4.2 on 2024-06-12 19:30

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='user',
            name='post_count',
            field=models.IntegerField(default=0),
        ),
    ]
