# Generated by Django 2.2.6 on 2019-10-15 15:17

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('UserLogin', '0005_auto_20190926_0649'),
    ]

    operations = [
        migrations.AddField(
            model_name='user',
            name='balance',
            field=models.IntegerField(default=True),
        ),
    ]
