# Generated by Django 5.0.7 on 2024-07-27 22:39

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('home', '0005_remove_post_blog_alter_post_date'),
    ]

    operations = [
        migrations.AlterField(
            model_name='post',
            name='date',
            field=models.DateField(default=datetime.datetime(2024, 7, 27, 22, 39, 3, 632577)),
        ),
    ]
