# Generated by Django 4.0 on 2022-05-27 17:04

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0010_user_user_currency'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='product',
            options={'ordering': ('last_update',)},
        ),
    ]
