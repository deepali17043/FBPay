# Generated by Django 2.2.6 on 2019-11-03 06:51

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('UserLogin', '0038_user_grpadm'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='user',
            name='grpadm',
        ),
    ]
