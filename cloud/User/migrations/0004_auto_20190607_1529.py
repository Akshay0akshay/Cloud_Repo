# Generated by Django 2.2.1 on 2019-06-07 09:59

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('User', '0003_auto_20190607_1519'),
    ]

    operations = [
        migrations.AlterField(
            model_name='encrypt',
            name='fid',
            field=models.IntegerField(),
        ),
    ]
