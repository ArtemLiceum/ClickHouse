import uuid
from django.db import models


class Category(models.Model):
    title = models.CharField(max_length=200)
    description = models.TextField(blank=True)


class Tag(models.Model):
    title = models.CharField(max_length=100)
    description = models.TextField(blank=True)


class Product(models.Model):
    category = models.ForeignKey(Category, on_delete=models.PROTECT, related_name="products")
    title = models.CharField(max_length=300)
    description = models.TextField(blank=True)
    tags = models.ManyToManyField(Tag, blank=True, related_name="products")
    price = models.IntegerField()


class Discount(models.Model):
    is_active = models.BooleanField(default=False)
    amount = models.IntegerField()
    category = models.ForeignKey(Category, on_delete=models.SET_NULL, null=True, blank=True)
    product = models.ForeignKey(Product, on_delete=models.SET_NULL, null=True, blank=True)


class Customer(models.Model):
    login = models.CharField(max_length=150, unique=True)
    name = models.CharField(max_length=150)
    last_name = models.CharField(max_length=150, blank=True)
    age = models.IntegerField(null=True, blank=True)


class Order(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    order_datetime = models.DateTimeField(db_index=True)
    customer = models.ForeignKey(Customer, on_delete=models.DO_NOTHING, related_name="orders")
    product = models.ForeignKey(Product, on_delete=models.DO_NOTHING, related_name="orders")
    amount = models.IntegerField()
    discount = models.IntegerField(default=0)
