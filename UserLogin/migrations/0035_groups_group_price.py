# Generated by Django 2.2.6 on 2019-10-29 14:31

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('UserLogin', '0034_remove_accountsummary_mn'),
    ]

    operations = [
        migrations.AddField(
            model_name='groups',
            name='group_price',
            field=models.IntegerField(default=0),
        ),
    ]