# Generated by Django 2.2.6 on 2019-10-21 06:20

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('UserLogin', '0024_user_timeline'),
    ]

    operations = [
        migrations.AddField(
            model_name='timeline',
            name='self',
            field=models.BooleanField(default=True),
        ),
    ]
