# Generated by Django 2.2.2 on 2019-07-03 06:16

from django.conf import settings
from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('main', '0005_auto_20190703_0005'),
    ]

    operations = [
        migrations.RenameModel(
            old_name='Activities',
            new_name='Activity',
        ),
        migrations.AlterUniqueTogether(
            name='activity',
            unique_together=set(),
        ),
    ]
