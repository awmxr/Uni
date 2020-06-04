# Generated by Django 3.0.6 on 2020-06-03 07:34

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('uni', '0009_remove_student_birthday'),
    ]

    operations = [
        migrations.AlterField(
            model_name='student',
            name='College',
            field=models.CharField(choices=[('فنی مهندسی', 'فنی مهندسی'), ('علوم پایه', 'علوم پایه'), ('اقتصاد', 'اقتصاد'), ('علوم سیاسی', 'علوم سیاسی'), ('اقیانوس', 'اقیانوس'), ('شیمی', 'شیمی')], max_length=200),
        ),
        migrations.AlterField(
            model_name='student',
            name='uni',
            field=models.CharField(choices=[('تهران', 'تهران'), ('مازندران', 'مازندران'), ('اصفهان', 'اصفهان'), ('امیرکبیر', 'امیر کبیر'), ('صنعتی شریف', 'صنعتی شریف'), ('شهید بهشتی', 'شهید بهشتی'), ('صنعتی اصفهان', 'صنعتی اصفهان'), ('علم و صنعت', 'علم و صنعت'), ('خواجه نصیر', 'خواجه نصیر'), ('شیراز', 'شیراز'), ('نوشیروانی', 'نوشیروانی'), ('تبریز', 'تبریز')], max_length=200),
        ),
    ]