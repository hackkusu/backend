# Generated by Django 2.1.7 on 2024-04-07 04:32

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('polls', '0003_auto_20240320_2141'),
    ]

    operations = [
        migrations.AlterModelTable(
            name='recipe',
            table='recipe',
        ),
        migrations.AlterModelTable(
            name='user',
            table='user',
        ),
        migrations.AlterModelTable(
            name='video',
            table='video',
        ),
    ]
