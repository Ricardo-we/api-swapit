# Generated by Django 4.0 on 2022-05-25 18:52

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0009_product_in_revision_report_product_reports'),
    ]

    operations = [
        migrations.AddField(
            model_name='user',
            name='user_currency',
            field=models.CharField(blank=True, default='Q', max_length=5, null=True),
        ),
    ]
