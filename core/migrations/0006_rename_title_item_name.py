# Generated by Django 4.2.17 on 2024-12-22 09:56

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0005_itemimage_features'),
    ]

    operations = [
        migrations.RenameField(
            model_name='item',
            old_name='title',
            new_name='name',
        ),
    ]
