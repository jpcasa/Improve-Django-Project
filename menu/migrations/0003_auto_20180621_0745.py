# Generated by Django 2.0.6 on 2018-06-21 14:45

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('menu', '0002_auto_20160406_1554'),
    ]

    operations = [
        migrations.AlterField(
            model_name='item',
            name='chef',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL),
        ),
    ]
