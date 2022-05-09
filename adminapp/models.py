from email.policy import default
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
    branch_name = models.CharField(max_length=50)
    branch_id = models.CharField(max_length=20)
    email = models.CharField(max_length=30)
    phone = models.CharField(max_length=18)
    place = models.CharField(max_length=50)
    address = models.CharField(max_length=200)
    status = models.CharField(max_length=15, default="Active")
    password = models.CharField(max_length=30)

    class Meta:
        db_table='branch'


class Staff(models.Model):
    name = models.CharField(max_length=50)
    staff_id = models.CharField(max_length=20)
    email = models.CharField(max_length=30)
    phone = models.CharField(max_length=18)
    place = models.CharField(max_length=50)
    state = models.CharField(max_length=50)
    pincode = models.CharField(max_length=15)
    address = models.CharField(max_length=200)
    date = models.DateField()
    branch = models.ForeignKey(Branch, on_delete=models.CASCADE)
    status = models.CharField(max_length=15,default="Active")

    class Meta:
        db_table='staff' 


class StaffBankDetails(models.Model):
    staff=models.ForeignKey(Staff,on_delete=models.CASCADE)
    holder_name=models.CharField(max_length=50)
    bank_name=models.CharField(max_length=150)
    account_number=models.CharField(max_length=50)
    ifsc=models.CharField(max_length=50)
    branch=models.CharField(max_length=150,default="")

    class Meta:
        db_table='staffbank'

class Transfer(models.Model):
    staff = models.ForeignKey(Staff, on_delete=models.CASCADE)
    from_branch = models.ForeignKey(Branch, on_delete=models.CASCADE, related_name='frombranch')
    to_branch = models.ForeignKey(Branch, on_delete=models.CASCADE, related_name='tobranch')
    from_date = models.DateField()
    to_date = models.DateField()
    status = models.CharField(max_length=20, default="requested")

    class Meta:
        db_table='transfer'

class Decline(models.Model):
    transfer_id = models.ForeignKey(Transfer,on_delete=models.PROTECT)
    msg = models.CharField(max_length=500)

    class Meta:
        db_table='decline'