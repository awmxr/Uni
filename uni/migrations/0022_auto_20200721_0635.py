# Generated by Django 3.0.7 on 2020-07-21 02:05

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('uni', '0021_forget_check'),
    ]

    operations = [
        migrations.AlterField(
            model_name='forget',
            name='college',
            field=models.CharField(blank=True, max_length=200),
        ),
    ]
