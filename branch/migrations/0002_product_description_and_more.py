# Generated by Django 4.0.4 on 2022-04-23 06:44

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('branch', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='product',
            name='description',
            field=models.CharField(default='Null', max_length=200),
        ),
        migrations.AlterField(
            model_name='branchproducts',
            name='purchase_date',
            field=models.DateField(default=datetime.date.today),
        ),
    ]
