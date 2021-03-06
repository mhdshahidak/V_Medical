# Generated by Django 4.0.4 on 2022-05-07 06:19

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('branch', '0018_alter_expense_date_alter_income_date'),
    ]

    operations = [
        migrations.AlterField(
            model_name='expense',
            name='date',
            field=models.DateTimeField(default=datetime.date.today),
        ),
        migrations.AlterField(
            model_name='income',
            name='date',
            field=models.DateField(default=datetime.date.today),
        ),
    ]
