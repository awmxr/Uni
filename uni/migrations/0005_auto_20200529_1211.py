# Generated by Django 3.0.6 on 2020-05-29 07:41

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('uni', '0004_auto_20200529_1208'),
    ]

    operations = [
        migrations.AddField(
            model_name='student',
            name='field',
            field=models.CharField(default=' ', max_length=200),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='student',
            name='parents_phone',
            field=models.CharField(default=' ', max_length=200),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='student',
            name='student_live',
            field=models.CharField(default=' ', max_length=200),
            preserve_default=False,
        ),
    ]