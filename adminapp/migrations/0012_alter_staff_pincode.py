# Generated by Django 4.0.4 on 2022-05-05 08:40

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('adminapp', '0011_remove_staff_profile'),
    ]

    operations = [
        migrations.AlterField(
            model_name='staff',
            name='pincode',
            field=models.CharField(max_length=15),
        ),
    ]