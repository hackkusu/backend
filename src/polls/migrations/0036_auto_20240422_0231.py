# Generated by Django 2.1.7 on 2024-04-22 02:31

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('polls', '0035_auto_20240422_0229'),
    ]

    operations = [
        migrations.AlterField(
            model_name='conversation',
            name='phone_number',
            field=models.CharField(db_column='phone_number', max_length=15),
        ),
    ]