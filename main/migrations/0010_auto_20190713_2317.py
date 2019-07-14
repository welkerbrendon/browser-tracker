# Generated by Django 2.2.2 on 2019-07-14 05:17

from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0009_auto_20190706_1623'),
    ]

    operations = [
        migrations.AddField(
            model_name='activitytype',
            name='created_at',
            field=models.DateTimeField(auto_now_add=True, default=django.utils.timezone.now),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='activitytype',
            name='last_updated',
            field=models.DateTimeField(auto_now=True),
        ),
    ]