# Generated by Django 3.2 on 2022-01-25 02:46

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('rates', '0009_auto_20220109_1907'),
    ]

    operations = [
        migrations.AlterField(
            model_name='ratereport',
            name='negotiated',
            field=models.BooleanField(default=False),
            preserve_default=False,
        ),
    ]
