# Generated by Django 3.2 on 2021-12-14 21:11

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('rates', '0003_auto_20211115_2020'),
    ]

    operations = [
        migrations.AlterField(
            model_name='rawratereport',
            name='job_title',
            field=models.CharField(max_length=36, null=True),
        ),
        migrations.AlterField(
            model_name='rawratereport',
            name='network',
            field=models.CharField(max_length=36, null=True),
        ),
        migrations.AlterField(
            model_name='rawratereport',
            name='show',
            field=models.CharField(max_length=36, null=True),
        ),
    ]
