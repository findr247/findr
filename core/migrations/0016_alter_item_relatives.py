# Generated by Django 4.2.17 on 2025-01-17 22:25

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0015_item_date_alter_item_location'),
    ]

    operations = [
        migrations.AlterField(
            model_name='item',
            name='relatives',
            field=models.ManyToManyField(blank=True, to='core.item'),
        ),
    ]
