# Generated by Django 2.0.3 on 2018-06-17 21:39

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('tree', '0011_auto_20180617_2048'),
    ]

    operations = [
        migrations.AlterModelTable(
            name='tree',
            table='tree',
        ),
        migrations.AlterModelTable(
            name='treeimages',
            table='tree_image',
        ),
        migrations.AlterModelTable(
            name='treesort',
            table='tree_sort',
        ),
        migrations.AlterModelTable(
            name='treetype',
            table='tree_type',
        ),
    ]
