# Generated by Django 4.2.17 on 2024-12-25 14:30

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0007_remove_item_category'),
    ]

    operations = [
        migrations.DeleteModel(
            name='Category',
        ),
    ]
