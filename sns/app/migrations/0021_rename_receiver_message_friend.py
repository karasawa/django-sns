# Generated by Django 3.2.6 on 2022-02-05 20:05

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0020_message_receiver'),
    ]

    operations = [
        migrations.RenameField(
            model_name='message',
            old_name='receiver',
            new_name='friend',
        ),
    ]
