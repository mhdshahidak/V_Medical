from django.db import models

# Create your models here.

class AdminLogin(models.Model):

    id = models.AutoField(primary_key=True)
    username = models.CharField(max_length=100)
    password = models.CharField(max_length=50)

    class Meta:  # to set table name
        db_table = "adminlogin"

