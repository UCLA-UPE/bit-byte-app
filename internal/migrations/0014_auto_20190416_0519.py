# Generated by Django 2.1.7 on 2019-04-16 05:19

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('internal', '0013_event_repeatable'),
    ]

    operations = [
        migrations.AlterField(
            model_name='profile',
            name='role',
            field=models.CharField(blank=True, choices=[('B', 'Byte'), ('b', 'Bit')], max_length=1, null=True),
        ),
    ]
