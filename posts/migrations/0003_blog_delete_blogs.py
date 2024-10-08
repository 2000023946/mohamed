# Generated by Django 5.0.7 on 2024-07-27 16:52

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('posts', '0002_alter_blogs_date'),
    ]

    operations = [
        migrations.CreateModel(
            name='Blog',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=100)),
                ('description', models.CharField(max_length=200)),
                ('date', models.DateField(blank=True, default=datetime.datetime(2024, 7, 27, 16, 52, 8, 610706))),
            ],
        ),
        migrations.DeleteModel(
            name='Blogs',
        ),
    ]
