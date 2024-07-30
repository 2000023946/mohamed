# Generated by Django 5.0.7 on 2024-07-28 23:29

import datetime
import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('posts', '0022_alter_blog_date'),
        ('welcome_page', '0009_remove_userprofile_recent_blogs_recent'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='recent',
            name='recent_blogs',
        ),
        migrations.AddField(
            model_name='recent',
            name='recent_blog',
            field=models.ForeignKey(blank=True, default=1, on_delete=django.db.models.deletion.CASCADE, to='posts.blog'),
        ),
        migrations.AlterField(
            model_name='recent',
            name='date',
            field=models.DateField(default=datetime.datetime(2024, 7, 28, 23, 29, 20, 627545)),
        ),
    ]
