# Generated by Django 3.2.6 on 2022-01-29 04:18

from django.db import migrations, models
import uuid


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='message',
            name='id',
            field=models.UUIDField(default=uuid.UUID('7b0712fe-089d-4637-9078-0a6063209102'), primary_key=True, serialize=False),
        ),
    ]
