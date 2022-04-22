from django.db import models

# Create your models here.



    
class AdminLogin(models.Model):

    id = models.AutoField(primary_key=True)
    username = models.CharField(max_length=100)
    password = models.CharField(max_length=50)

    class Meta:  # to set table name
        db_table = "adminlogin"


class Branch(models.Model):
    # id=models.AutoField(primary_key=True)
    branch_name=models.CharField(max_length=50)
    branch_id=models.CharField(max_length=20)
    email=models.CharField(max_length=30)
    phone=models.CharField(max_length=18)
    place=models.CharField(max_length=50)
    address=models.CharField(max_length=200)
    password=models.CharField(max_length=30)

    class Meta:
        db_table='branch'