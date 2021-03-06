# Generated by Django 2.1.7 on 2019-04-22 00:48

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('internal', '0014_auto_20190416_0519'),
    ]

    operations = [
        migrations.AddField(
            model_name='team',
            name='invite_code',
            field=models.CharField(default='AAA123', max_length=16),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='profile',
            name='user',
            field=models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, related_name='profile', to=settings.AUTH_USER_MODEL),
        ),
    ]
