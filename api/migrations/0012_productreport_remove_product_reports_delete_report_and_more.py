# Generated by Django 4.0 on 2022-05-27 18:12

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0011_alter_product_options'),
    ]

    operations = [
        migrations.CreateModel(
            name='ProductReport',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('report_reason', models.TextField(default='Is not', max_length=700)),
            ],
        ),
        migrations.RemoveField(
            model_name='product',
            name='reports',
        ),
        migrations.DeleteModel(
            name='Report',
        ),
        migrations.AddField(
            model_name='productreport',
            name='product',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='product', to='api.product'),
        ),
        migrations.AddField(
            model_name='productreport',
            name='report_from',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='api.user'),
        ),
    ]