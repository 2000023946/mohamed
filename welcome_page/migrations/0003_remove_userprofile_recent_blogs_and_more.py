# Generated by Django 5.0.7 on 2024-07-28 21:33

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('welcome_page', '0002_alter_userprofile_recent_blogs'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='userprofile',
            name='recent_blogs',
        ),
        migrations.RemoveField(
            model_name='userprofile',
            name='user',
        ),
        migrations.DeleteModel(
            name='Recent',
        ),
        migrations.DeleteModel(
            name='userProfile',
        ),
    ]
