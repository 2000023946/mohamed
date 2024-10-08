# Generated by Django 5.0.7 on 2024-07-28 23:17

import datetime
import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('posts', '0021_alter_blog_date'),
        ('welcome_page', '0008_remove_userprofile_recent_blogs_and_more'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='userprofile',
            name='recent_blogs',
        ),
        migrations.CreateModel(
            name='Recent',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('date', models.DateField(default=datetime.datetime(2024, 7, 28, 23, 17, 15, 936107))),
                ('recent_blogs', models.ManyToManyField(blank=True, default=1, to='posts.blog')),
                ('user_for', models.ForeignKey(blank=True, default=1, on_delete=django.db.models.deletion.CASCADE, related_name='recents', to='welcome_page.userprofile')),
            ],
        ),
    ]
