from django.contrib.postgres.operations import TrigramExtension
from django.db import migrations


class Migration(migrations.Migration):
    dependencies = [
        ('rates', '0014_auto_20220207_1204')
    ]
    operations = [
        TrigramExtension(),
    ]