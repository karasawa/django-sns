# Generated by Django 3.2.6 on 2022-01-30 05:16

from django.db import migrations, models
import uuid


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0014_auto_20220130_1323'),
    ]

    operations = [
        migrations.AlterField(
            model_name='friend',
            name='id',
            field=models.UUIDField(default=uuid.uuid4, primary_key=True, serialize=False),
        ),
    ]
