# Generated by Django 4.0 on 2022-05-21 20:01

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0005_alter_user_location'),
    ]

    operations = [
        migrations.CreateModel(
            name='ConfirmationCode',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('username', models.CharField(max_length=150, unique=True)),
                ('code', models.CharField(max_length=4)),
            ],
        ),
    ]
