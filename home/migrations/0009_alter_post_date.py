# Generated by Django 5.0.7 on 2024-07-28 20:20

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('home', '0008_alter_post_date'),
    ]

    operations = [
        migrations.AlterField(
            model_name='post',
            name='date',
            field=models.DateField(default=datetime.datetime(2024, 7, 28, 20, 20, 34, 222036)),
        ),
    ]
