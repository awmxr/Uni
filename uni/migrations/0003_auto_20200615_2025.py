# Generated by Django 3.0.7 on 2020-06-15 15:55

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('uni', '0002_auto_20200615_2011'),
    ]

    operations = [
        migrations.AddField(
            model_name='elam',
            name='dascode',
            field=models.CharField(default=' ', max_length=1000),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='elam',
            name='groh',
            field=models.CharField(default=' ', max_length=1000),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='klass',
            name='t01',
            field=models.CharField(blank=True, max_length=200),
        ),
        migrations.AlterField(
            model_name='klass',
            name='t02',
            field=models.CharField(blank=True, max_length=200),
        ),
        migrations.AlterField(
            model_name='klass',
            name='t03',
            field=models.CharField(blank=True, max_length=200),
        ),
        migrations.AlterField(
            model_name='klass',
            name='t04',
            field=models.CharField(blank=True, max_length=200),
        ),
        migrations.AlterField(
            model_name='klass',
            name='t05',
            field=models.CharField(blank=True, max_length=200),
        ),
        migrations.AlterField(
            model_name='klass',
            name='t11',
            field=models.CharField(blank=True, max_length=200),
        ),
        migrations.AlterField(
            model_name='klass',
            name='t12',
            field=models.CharField(blank=True, max_length=200),
        ),
        migrations.AlterField(
            model_name='klass',
            name='t13',
            field=models.CharField(blank=True, max_length=200),
        ),
        migrations.AlterField(
            model_name='klass',
            name='t14',
            field=models.CharField(blank=True, max_length=200),
        ),
        migrations.AlterField(
            model_name='klass',
            name='t15',
            field=models.CharField(blank=True, max_length=200),
        ),
        migrations.AlterField(
            model_name='klass',
            name='t21',
            field=models.CharField(blank=True, max_length=200),
        ),
        migrations.AlterField(
            model_name='klass',
            name='t22',
            field=models.CharField(blank=True, max_length=200),
        ),
        migrations.AlterField(
            model_name='klass',
            name='t23',
            field=models.CharField(blank=True, max_length=200),
        ),
        migrations.AlterField(
            model_name='klass',
            name='t24',
            field=models.CharField(blank=True, max_length=200),
        ),
        migrations.AlterField(
            model_name='klass',
            name='t25',
            field=models.CharField(blank=True, max_length=200),
        ),
        migrations.AlterField(
            model_name='klass',
            name='t31',
            field=models.CharField(blank=True, max_length=200),
        ),
        migrations.AlterField(
            model_name='klass',
            name='t32',
            field=models.CharField(blank=True, max_length=200),
        ),
        migrations.AlterField(
            model_name='klass',
            name='t33',
            field=models.CharField(blank=True, max_length=200),
        ),
        migrations.AlterField(
            model_name='klass',
            name='t34',
            field=models.CharField(blank=True, max_length=200),
        ),
        migrations.AlterField(
            model_name='klass',
            name='t35',
            field=models.CharField(blank=True, max_length=200),
        ),
        migrations.AlterField(
            model_name='klass',
            name='t41',
            field=models.CharField(blank=True, max_length=200),
        ),
        migrations.AlterField(
            model_name='klass',
            name='t42',
            field=models.CharField(blank=True, max_length=200),
        ),
        migrations.AlterField(
            model_name='klass',
            name='t43',
            field=models.CharField(blank=True, max_length=200),
        ),
        migrations.AlterField(
            model_name='klass',
            name='t44',
            field=models.CharField(blank=True, max_length=200),
        ),
        migrations.AlterField(
            model_name='klass',
            name='t45',
            field=models.CharField(blank=True, max_length=200),
        ),
    ]