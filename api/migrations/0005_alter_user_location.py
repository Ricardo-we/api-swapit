# Generated by Django 4.0 on 2022-05-21 01:04

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0004_producttags_product_tags'),
    ]

    operations = [
        migrations.AlterField(
            model_name='user',
            name='location',
            field=models.CharField(blank=True, max_length=150, null=True),
        ),
    ]
