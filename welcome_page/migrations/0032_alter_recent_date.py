# Generated by Django 5.1 on 2024-09-10 17:25

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('welcome_page', '0031_alter_recent_date'),
    ]

    operations = [
        migrations.AlterField(
            model_name='recent',
            name='date',
            field=models.DateField(default=datetime.datetime(2024, 9, 10, 17, 25, 35, 39083)),
        ),
    ]
