# Generated by Django 2.1.7 on 2019-04-28 10:03

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('internal', '0017_auto_20190428_0953'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='event',
            name='points',
        ),
        migrations.RemoveField(
            model_name='event',
            name='repeatable',
        ),
        migrations.RemoveField(
            model_name='eventcheckoff',
            name='event',
        ),
    ]
