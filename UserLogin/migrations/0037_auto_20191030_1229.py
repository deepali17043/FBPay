# Generated by Django 2.2.6 on 2019-10-30 12:29

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('UserLogin', '0036_auto_20191030_1219'),
    ]

    operations = [
        migrations.AlterField(
            model_name='user',
            name='Birthday',
            field=models.CharField(max_length=10),
        ),
    ]
