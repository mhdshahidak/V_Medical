# Generated by Django 4.0.4 on 2022-05-07 05:18

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('branch', '0016_invoive_grand_total_invoive_gst'),
    ]

    operations = [
        migrations.RenameField(
            model_name='income',
            old_name='amount',
            new_name='incomeamount',
        ),
    ]
