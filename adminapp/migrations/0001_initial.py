# Generated by Django 4.0.4 on 2022-04-22 06:17

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='AdminLogin',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('username', models.CharField(max_length=100)),
                ('password', models.CharField(max_length=50)),
            ],
            options={
                'db_table': 'adminlogin',
            },
        ),
    ]
