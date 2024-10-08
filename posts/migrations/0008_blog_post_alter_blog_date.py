# Generated by Django 5.0.7 on 2024-07-27 22:31

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('home', '0005_remove_post_blog_alter_post_date'),
        ('posts', '0007_alter_blog_date'),
    ]

    operations = [
        migrations.AddField(
            model_name='blog',
            name='post',
            field=models.ManyToManyField(to='home.post'),
        ),
        migrations.AlterField(
            model_name='blog',
            name='date',
            field=models.DateField(blank=True, default=datetime.datetime(2024, 7, 27, 22, 31, 19, 201300)),
        ),
    ]
