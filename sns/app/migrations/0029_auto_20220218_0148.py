# Generated by Django 3.2.6 on 2022-02-17 16:48

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0028_message_profile'),
    ]

    operations = [
        migrations.AddField(
            model_name='friend',
            name='profile_send_from',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='profile_send_from', to='app.profile'),
        ),
        migrations.AddField(
            model_name='friend',
            name='profile_send_to',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='app.profile'),
        ),
    ]
