# Generated by Django 3.2.6 on 2022-01-31 16:14

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0015_alter_friend_id'),
    ]

    operations = [
        migrations.AddField(
            model_name='group',
            name='icon',
            field=models.ImageField(blank=True, null=True, upload_to=''),
        ),
    ]
