# Generated by Django 5.0.7 on 2024-07-28 21:50

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('posts', '0015_remove_blog_users_alter_blog_date'),
        ('welcome_page', '0003_remove_userprofile_recent_blogs_and_more'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='userProfile',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('blogs_in', models.IntegerField(default=0)),
                ('recent_blogs', models.ManyToManyField(to='posts.blog')),
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
