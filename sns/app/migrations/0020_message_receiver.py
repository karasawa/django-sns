# Generated by Django 3.2.6 on 2022-02-05 20:01

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0019_auto_20220205_1620'),
    ]

    operations = [
        migrations.AddField(
            model_name='message',
            name='receiver',
            field=models.CharField(blank=True, max_length=30, null=True),
        ),
    ]