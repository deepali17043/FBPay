# Generated by Django 2.2.6 on 2019-10-18 17:30

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('UserLogin', '0017_auto_20191018_1725'),
    ]

    operations = [
        migrations.AlterField(
            model_name='user',
            name='balance',
            field=models.IntegerField(default=True),
        ),
    ]