# Generated by Django 5.1.1 on 2024-11-09 00:40

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('bodhidharaAPI', '0002_bodhidharanews_views'),
    ]

    operations = [
        migrations.AlterField(
            model_name='bodhidharanews',
            name='views',
            field=models.JSONField(default=list),
        ),
    ]
