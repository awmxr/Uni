# Generated by Django 3.0.6 on 2020-06-05 06:36

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('uni', '0005_student_birthday'),
    ]

    operations = [
        migrations.AlterField(
            model_name='student',
            name='public_date',
            field=models.DateTimeField(null=True),
        ),
    ]
