# Generated by Django 5.0.7 on 2024-07-28 23:45

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('posts', '0022_alter_blog_date'),
    ]

    operations = [
        migrations.AlterField(
            model_name='blog',
            name='date',
            field=models.DateField(blank=True, default=datetime.datetime(2024, 7, 28, 23, 45, 40, 49208)),
        ),
    ]
