# Generated by Django 3.0.6 on 2020-06-05 04:41

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Admin',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('Admin_username', models.CharField(max_length=200)),
                ('admin_name', models.CharField(max_length=200)),
                ('admin_last_name', models.CharField(max_length=200)),
                ('admin_password', models.CharField(max_length=200)),
                ('pub_date', models.DateTimeField(verbose_name='date published')),
            ],
        ),
        migrations.CreateModel(
            name='Exter',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('exter_name', models.CharField(max_length=200)),
                ('number', models.CharField(max_length=200)),
            ],
        ),
        migrations.CreateModel(
            name='Student',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('username', models.CharField(max_length=200)),
                ('name', models.CharField(max_length=200)),
                ('father_name', models.CharField(max_length=200)),
                ('melli_code', models.CharField(max_length=200)),
                ('enter_year', models.CharField(max_length=200)),
                ('uni', models.CharField(max_length=200)),
                ('College', models.CharField(max_length=200)),
                ('last_name', models.CharField(max_length=200)),
                ('password', models.CharField(max_length=200)),
                ('phone', models.CharField(max_length=11)),
                ('field', models.CharField(max_length=200)),
                ('student_live', models.CharField(max_length=200)),
                ('parents_phone', models.CharField(max_length=200)),
                ('religion', models.CharField(max_length=200)),
                ('birthday', models.DateTimeField(verbose_name='birthday')),
            ],
        ),
    ]
