# Generated by Django 3.0.7 on 2020-07-16 15:06

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('uni', '0020_student_sex'),
    ]

    operations = [
        migrations.AlterField(
            model_name='student',
            name='sex',
            field=models.CharField(blank=True, max_length=200),
        ),
    ]
