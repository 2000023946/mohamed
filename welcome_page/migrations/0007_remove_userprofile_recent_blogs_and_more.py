# Generated by Django 5.0.7 on 2024-07-28 22:43

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('posts', '0019_alter_blog_date'),
        ('welcome_page', '0006_alter_userprofile_recent_blogs'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='userprofile',
            name='recent_blogs',
        ),
        migrations.AddField(
            model_name='userprofile',
            name='recent_blogs',
            field=models.ForeignKey(blank=True, default=1, on_delete=django.db.models.deletion.CASCADE, to='posts.blog'),
        ),
    ]
