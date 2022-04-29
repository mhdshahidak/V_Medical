import datetime
from unicodedata import category
from django.db import models

from adminapp.models import Branch

# Create your models here.

class Product(models.Model):
    product_id = models.CharField(max_length=20)
    name = models.CharField(max_length=100)
    purchase_cost = models.IntegerField()
    selling_cost = models.IntegerField()
    description = models.CharField(max_length=200, default="Null")

    class Meta:
        db_table = 'product'

class BranchProducts(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    purchase_date = models.DateField(default=datetime.date.today)
    expiry_date = models.DateField()
    quantity = models.IntegerField(default=0)
    branch = models.ForeignKey(Branch, on_delete=models.CASCADE)

    class Meta:
        db_table = 'branchproducts'
        unique_together = ('product','branch')
    


class Customers(models.Model):
    name = models.CharField(max_length = 30)
    phone = models.CharField(max_length = 15)
    email = models.CharField(max_length = 50)
    place = models.CharField(max_length = 60)

    class Meta:
        db_table = 'customers'


class BranchBank(models.Model):
    branch=models.ForeignKey(Branch,on_delete=models.CASCADE)
    Accholder_name=models.CharField(max_length=70)
    account_number=models.CharField(max_length=50)
    bank_name=models.CharField(max_length=50)
    branch_name=models.CharField(max_length=50)
    ifsc=models.CharField(max_length=30)
    bankbalane=models.FloatField(default=0)

    class Meta:
        db_table = 'branchbank'


class MedicineTransfer(models.Model):
    reqbranch = models.ForeignKey(Branch, on_delete=models.CASCADE)
    avblbranch = models.ForeignKey(BranchProducts, related_name='availablebranch', on_delete=models.CASCADE)
    quantity = models.IntegerField()
    reqdate = models.DateField(default=datetime.date.today)
    status = models.CharField(max_length=20, default='Requested')

    class Meta:
        db_table = 'medtransfer'


class Expense(models.Model):
    category=models.CharField(max_length=50)
    date=models.DateField(default=datetime.date.today)
    note=models.CharField(max_length=500)
    amount=models.FloatField()
    branch_id=models.ForeignKey(Branch,on_delete=models.CASCADE)

    class Meta:
        db_table='expense'


class Invoive(models.Model):
    invoice_no = models.CharField(max_length=15,unique=True)
    customer = models.ForeignKey(Customers, on_delete=models.CASCADE)
    date = models.DateField(default=datetime.date.today)
    product = models.ForeignKey(BranchProducts, on_delete=models.CASCADE)
    quantity = models.IntegerField()
    total = models.IntegerField()
    payment_methode = models.CharField(max_length=30)

    class Meta:
        db_table = 'invoice'


class Income(models.Model):
    category=models.CharField(max_length=50)
    date=models.DateField(default=datetime.date.today)
    note=models.CharField(max_length=500)
    amount=models.FloatField()
    criteria=models.CharField(max_length=250)
    fromperson=models.CharField(max_length=25)
    branch_id=models.ForeignKey(Branch,on_delete=models.CASCADE)
    
    class Meta:
        db_table = 'income'

