# Generated by Django 4.0.4 on 2022-04-23 04:05

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('adminapp', '0004_staff_status'),
    ]

    operations = [
        migrations.AddField(
            model_name='branch',
            name='status',
            field=models.CharField(default='Active', max_length=15),
        ),
    ]
