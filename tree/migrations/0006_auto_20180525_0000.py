# Generated by Django 2.0.3 on 2018-05-24 21:00

from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('tree', '0005_auto_20180524_1357'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='tree',
            name='confirms',
        ),
        migrations.AddField(
            model_name='tree',
            name='confirms',
            field=models.ManyToManyField(to=settings.AUTH_USER_MODEL),
        ),
    ]