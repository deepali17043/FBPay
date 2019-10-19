# Generated by Django 2.2.6 on 2019-10-18 21:03

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('UserLogin', '0022_timeline_datetime'),
    ]

    operations = [
        migrations.AddField(
            model_name='user',
            name='type',
            field=models.IntegerField(default=1),
        ),
        migrations.AlterField(
            model_name='friendshiprequest',
            name='from_user',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='inv_from', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AlterField(
            model_name='friendshiprequest',
            name='to_user',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='inv_to', to=settings.AUTH_USER_MODEL),
        ),
        migrations.CreateModel(
            name='Groups',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('group_name', models.CharField(max_length=200)),
                ('group_closed', models.BooleanField(default=False)),
                ('group_admin', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='grp_admin1', to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='GroupRequest',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('acc', models.BooleanField(default=False)),
                ('fro', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='from_r', to=settings.AUTH_USER_MODEL)),
                ('group', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='to_r', to='UserLogin.Groups')),
            ],
        ),
        migrations.CreateModel(
            name='Group_messages',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('message', models.CharField(max_length=2500)),
                ('datetime', models.DateTimeField(auto_now=True)),
                ('group', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='grp_name1', to='UserLogin.Groups')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='grp_mem1', to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Group_mem',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('group', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='grp_name', to='UserLogin.Groups')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='grp_mem', to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
