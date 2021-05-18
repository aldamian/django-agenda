# Generated by Django 2.2 on 2021-05-17 08:58

import datetime
from django.db import migrations, models
from django.utils.timezone import utc


class Migration(migrations.Migration):

    dependencies = [
        ('agenda', '0005_auto_20210514_1638'),
    ]

    operations = [
        migrations.AddField(
            model_name='agenda',
            name='content',
            field=models.TextField(default='Enter your text here'),
        ),
        migrations.AlterField(
            model_name='agenda',
            name='notify_me_at',
            field=models.DateTimeField(default=datetime.datetime(2021, 5, 18, 6, 0, tzinfo=utc)),
        ),
    ]