from django.db import models

from adminapp.models import Branch

# Create your models here.

class Product(models.Model):
    product_id = models.CharField(max_length=20)
    name = models.CharField(max_length=100)
    purchase_cost = models.IntegerField()
    selling_cost = models.IntegerField()

    class Meta:
        db_table = 'product'

class BranchProducts(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    purchase_date = models.DateField()
    expiry_date = models.DateField()
    branch = models.ForeignKey(Branch, on_delete=models.CASCADE)

    class Meta:
        db_table = 'branchproducts'
