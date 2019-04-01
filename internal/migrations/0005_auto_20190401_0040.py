# Generated by Django 2.1.7 on 2019-04-01 00:40

import django.contrib.postgres.fields.jsonb
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('internal', '0004_auto_20190326_1920'),
    ]

    operations = [
        migrations.CreateModel(
            name='Event',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=200)),
                ('points', models.IntegerField()),
            ],
        ),
        migrations.CreateModel(
            name='EventCheckoff',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('event', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='internal.Event')),
            ],
        ),
        migrations.CreateModel(
            name='Team',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=200)),
            ],
        ),
        migrations.AlterField(
            model_name='profile',
            name='answers',
            field=django.contrib.postgres.fields.jsonb.JSONField(blank=True, default=list),
        ),
        migrations.AlterField(
            model_name='profile',
            name='role',
            field=models.CharField(choices=[('B', 'Byte'), ('b', 'Bit')], max_length=1),
        ),
        migrations.AddField(
            model_name='team',
            name='byte',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='internal.Profile'),
        ),
        migrations.AddField(
            model_name='eventcheckoff',
            name='person',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='internal.Profile'),
        ),
    ]
