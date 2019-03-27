# Generated by Django 2.1.7 on 2019-03-26 19:07

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('internal', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='SiteSettings',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('byte_signup_pass', models.CharField(default='upe_byte', max_length=255)),
                ('bit_signup_pass', models.CharField(default='bits_2019', max_length=255)),
            ],
            options={
                'abstract': False,
            },
        ),
    ]
