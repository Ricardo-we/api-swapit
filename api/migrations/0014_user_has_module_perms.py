# Generated by Django 4.0 on 2022-05-28 02:26

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0013_user_is_staff'),
    ]

    operations = [
        migrations.AddField(
            model_name='user',
            name='has_module_perms',
            field=models.BooleanField(default=False),
        ),
    ]