# Generated by Django 5.0.7 on 2024-07-27 22:52

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('home', '0006_alter_post_date'),
    ]

    operations = [
        migrations.AlterField(
            model_name='post',
            name='date',
            field=models.DateField(default=datetime.datetime(2024, 7, 27, 22, 52, 48, 555639)),
        ),
        migrations.AlterField(
            model_name='post',
            name='username',
            field=models.CharField(max_length=100),
        ),
    ]
