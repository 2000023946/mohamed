# Generated by Django 5.0.7 on 2024-07-28 22:06

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('welcome_page', '0004_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='userprofile',
            name='blogs_in',
        ),
    ]
