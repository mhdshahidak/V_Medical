# Generated by Django 4.0.4 on 2022-04-30 05:13

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('branch', '0011_alter_invoive_invoice_no'),
    ]

    operations = [
        migrations.AlterField(
            model_name='invoive',
            name='invoice_no',
            field=models.CharField(max_length=15),
        ),
    ]