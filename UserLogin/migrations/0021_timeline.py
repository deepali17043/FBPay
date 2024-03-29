# Generated by Django 2.2.6 on 2019-10-18 18:03

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('UserLogin', '0020_auto_20191018_1741'),
    ]

    operations = [
        migrations.CreateModel(
            name='Timeline',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('post', models.CharField(max_length=2500)),
                ('privacy', models.BooleanField(default=False)),
                ('from_t', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='from_t1', to=settings.AUTH_USER_MODEL)),
                ('to_t', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='to_t2', to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
