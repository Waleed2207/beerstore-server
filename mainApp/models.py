from django.db import models
from django.contrib.auth.models import User

TYPE_CHOICES = (("1", "Store manager"),
                ("2", "Store Employee"))


class UserProfile(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    username = models.CharField(max_length=32)
    firstName = models.CharField(max_length=32)
    lastName = models.CharField(max_length=32)
    email = models.CharField(max_length=200)
    userType = models.CharField(
        max_length=20,
        choices=TYPE_CHOICES,
        default='1'
    )

    def __str__(self):
        return self.user.username


class Products(models.Model):

    name = models.CharField(max_length=32)
    supplier_name = models.CharField(max_length=32)
    amount = models.DecimalField(max_digits=10, decimal_places=3)
    price = models.DecimalField(max_digits=10, decimal_places=3)

    def __str__(self):
        return self.name


class Suppliers(models.Model):
    name = models.CharField(max_length=32)
    SupplierEmail = models.EmailField(max_length=254, null=True)
    Products = models.ManyToManyField(Products, related_name='Products')
    address = models.CharField(max_length=32)


class Orders(models.Model):
    delivery_name = models.CharField(max_length=32)
    products = models.ManyToManyField('Products', related_name='orders')
    total_price = models.DecimalField(max_digits=10, decimal_places=3)
    order_date = models.DateField(null=True)
    delivery_date = models.DateField(null=True)
    address = models.CharField(max_length=32)
    amount = models.DecimalField(max_digits=10, decimal_places=3, null=True)
    status = models.BooleanField(default=False)
    
    def __str__(self):
        return f"Order #{self.pk} - {self.delivery_name}"
    