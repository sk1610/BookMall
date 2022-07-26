# Generated by Django 3.2.3 on 2021-07-14 11:40

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='book_table',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('book_name', models.CharField(max_length=100)),
                ('book_price', models.IntegerField(default=0)),
                ('book_image', models.ImageField(default='', upload_to='BookKharido/bookimages')),
                ('book_category', models.CharField(default='', max_length=100)),
                ('book_subcategory', models.CharField(default='', max_length=100)),
                ('book_author', models.CharField(default='', max_length=1000)),
                ('book_quantity', models.IntegerField()),
            ],
        ),
    ]
