# Generated by Django 4.0.4 on 2022-04-25 06:04

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('adminapp', '0005_branch_status'),
    ]

    operations = [
        migrations.AddField(
            model_name='staff',
            name='profile',
            field=models.ImageField(default='default.png', upload_to='staff/'),
        ),
    ]
