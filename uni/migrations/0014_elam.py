# Generated by Django 3.0.7 on 2020-06-14 08:48

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('uni', '0013_admin_college'),
    ]

    operations = [
        migrations.CreateModel(
            name='Elam',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('ostad', models.CharField(max_length=200)),
                ('college', models.CharField(max_length=200)),
                ('fields', models.CharField(max_length=200)),
                ('dars', models.CharField(max_length=200)),
                ('numbers', models.CharField(max_length=200)),
                ('capacity', models.CharField(max_length=200)),
                ('time', models.CharField(max_length=200)),
                ('public_date', models.DateTimeField(null=True)),
            ],
        ),
    ]