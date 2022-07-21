# Generated by Django 3.2.5 on 2021-07-25 12:51

from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('BookKharido', '0004_orders_cur'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='orders',
            name='cur',
        ),
        migrations.AddField(
            model_name='orders',
            name='currentdate',
            field=models.DateField(default=django.utils.timezone.now),
        ),
        migrations.AddField(
            model_name='orders',
            name='currenttime',
            field=models.TimeField(default=django.utils.timezone.now),
        ),
    ]