# Generated by Django 2.2.2 on 2019-07-03 03:13

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0003_auto_20190621_1238'),
    ]

    operations = [
        migrations.AddField(
            model_name='activitytype',
            name='universal',
            field=models.BooleanField(default=True),
        ),
        migrations.CreateModel(
            name='CombinedActivites',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('last_updated', models.DateTimeField(auto_now=True)),
                ('first_activity', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='first_activity', to='main.Activities')),
                ('second_activity', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='second_activity', to='main.Activities')),
            ],
        ),
    ]