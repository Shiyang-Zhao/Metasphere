# Generated by Django 5.0.4 on 2024-06-11 15:53

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('chats', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='chat',
            name='is_active',
            field=models.BooleanField(default=True),
        ),
    ]