# Generated by Django 3.2 on 2022-02-10 04:11

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('rates', '0004_auto_20220209_1211'),
    ]

    operations = [
        migrations.AlterField(
            model_name='ratereport',
            name='raw_report',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='rates.rawratereport'),
        ),
    ]
