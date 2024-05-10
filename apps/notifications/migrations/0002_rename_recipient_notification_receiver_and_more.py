# Generated by Django 5.0.4 on 2024-05-09 06:51

import django.db.models.deletion
import django.utils.timezone
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('notifications', '0001_initial'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.RenameField(
            model_name='notification',
            old_name='recipient',
            new_name='receiver',
        ),
        migrations.RemoveField(
            model_name='notification',
            name='text',
        ),
        migrations.AddField(
            model_name='notification',
            name='content',
            field=models.TextField(default='You have a new notification.'),
        ),
        migrations.AlterField(
            model_name='notification',
            name='created_at',
            field=models.DateTimeField(default=django.utils.timezone.now),
        ),
        migrations.AlterField(
            model_name='notification',
            name='notification_type',
            field=models.CharField(choices=[('message', 'Message'), ('friend_request', 'Friend Request'), ('system_alert', 'System Alert'), ('event_reminder', 'Event Reminder')], max_length=15),
        ),
        migrations.AlterField(
            model_name='notification',
            name='sender',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='sent_notifications', to=settings.AUTH_USER_MODEL),
        ),
    ]