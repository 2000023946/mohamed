# Generated by Django 5.0.7 on 2024-07-30 16:52

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('welcome_page', '0030_alter_recent_date'),
    ]

    operations = [
        migrations.AlterField(
            model_name='recent',
            name='date',
            field=models.DateField(default=datetime.datetime(2024, 7, 30, 16, 52, 52, 659852)),
        ),
    ]
