# Generated by Django 2.0.3 on 2018-06-24 17:48

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('tree', '0012_auto_20180618_0039'),
    ]

    operations = [
        migrations.RenameField(
            model_name='tree',
            old_name='active',
            new_name='is_active',
        ),
    ]