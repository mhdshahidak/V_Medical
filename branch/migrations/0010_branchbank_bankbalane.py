# Generated by Django 4.0.4 on 2022-04-29 09:56

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('branch', '0009_expense'),
    ]

    operations = [
        migrations.AddField(
            model_name='branchbank',
            name='bankbalane',
            field=models.FloatField(default=0),
        ),
    ]
