# Generated by Django 2.2.6 on 2019-10-16 04:20

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('UserLogin', '0007_user_authen'),
    ]

    operations = [
        migrations.RenameField(
            model_name='user',
            old_name='authen',
            new_name='authenticated',
        ),
    ]
