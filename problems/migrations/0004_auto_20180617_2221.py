# Generated by Django 2.0.3 on 2018-06-17 19:21

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('problems', '0003_auto_20180616_0033'),
    ]

    operations = [
        migrations.RenameModel(
            old_name='ProblemPhoto',
            new_name='ProblemImage',
        ),
    ]
