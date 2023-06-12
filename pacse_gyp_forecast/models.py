from django.db import models

# Create your models here.
class Category(models.Model):
    id = models.BigAutoField(primary_key=True)
    description = models.CharField(max_length=30)

class Status(models.Model):
    id = models.BigAutoField(primary_key=True)
    name = models.CharField(max_length=50)

class Product(models.Model):
    id = models.BigAutoField(primary_key=True)
    SKU = models.CharField(max_length=30, unique=True)
    description = models.CharField(max_length=100)
    restock_time = models.IntegerField()
    ignored = models.BooleanField(default=False)
    deleted = models.BooleanField(default=False)
    known = models.BooleanField(default=False)
    #FK attributes.
    Category = models.ForeignKey(Category, on_delete=models.CASCADE)
    Status = models.ForeignKey(Status, on_delete=models.CASCADE)

class Stock(models.Model):
    id = models.BigAutoField(primary_key=True)
    quantity = models.IntegerField()
    date = models.DateField()
    #FK attributes.
    Product = models.ForeignKey(Product, on_delete=models.CASCADE)

class Sales(models.Model):
    id = models.BigAutoField(primary_key=True)
    date = models.DateTimeField()
    units = models.IntegerField()
    #FK attributes.
    Product = models.ForeignKey(Product, on_delete=models.CASCADE)

class Forecast(models.Model):
    id = models.BigAutoField(primary_key=True)
    date = models.DateField()
    units = models.IntegerField()
    #FK attributes.
    Product = models.ForeignKey(Product, on_delete=models.CASCADE)

class Role(models.Model):
    id = models.BigAutoField(primary_key=True)
    name = models.CharField(max_length=30)

class User(models.Model):
    id = models.BigAutoField(primary_key=True)
    name = models.CharField(max_length=30)
    deleted = models.BooleanField(default=False)

class Credential(models.Model):
    id = models.BigAutoField(primary_key=True)
    email = models.CharField()
    password = models.CharField(max_length=30)
    #FK attributes.
    User = models.ForeignKey(User, on_delete=models.CASCADE)
