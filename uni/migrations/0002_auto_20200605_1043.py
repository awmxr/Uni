# Generated by Django 3.0.6 on 2020-06-05 06:13

import datetime
from django.db import migrations, models
from django.utils.timezone import utc


class Migration(migrations.Migration):

    dependencies = [
        ('uni', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='student',
            name='public_date',
            field=models.DateTimeField(default=datetime.datetime(2020, 6, 5, 6, 13, 57, 913909, tzinfo=utc)),
        ),
        migrations.AlterField(
            model_name='student',
            name='birthday',
            field=models.DateField(default=None),
        ),
    ]
