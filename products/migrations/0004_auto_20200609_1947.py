# Generated by Django 2.2.13 on 2020-06-09 16:47

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('products', '0003_auto_20200603_1546'),
    ]

    operations = [
        migrations.RenameField(
            model_name='tovar',
            old_name='price',
            new_name='unit_price',
        ),
    ]