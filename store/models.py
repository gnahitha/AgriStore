from django.db import models

class Product(models.Model):
    name = models.CharField(max_length=100)
    price = models.IntegerField()
    stock = models.IntegerField()
    description = models.TextField()
    image = models.CharField(max_length=200, blank=True, null=True)
    category = models.CharField(max_length=50, default="grains")
    seller_name = models.CharField(max_length=100, default="Agri Store")

    seller_phone = models.CharField(max_length=15, default="9876543210")

    seller_email = models.EmailField(default="agristore@gmail.com")

    def __str__(self):
        return self.name


class Review(models.Model):

    product = models.ForeignKey(
        Product,
        on_delete=models.CASCADE
    )

    name = models.CharField(max_length=100)

    rating = models.IntegerField()

    comment = models.TextField()

    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.product.name
from django.contrib.auth.models import User

class Wishlist(models.Model):

    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE
    )

    product = models.ForeignKey(
        Product,
        on_delete=models.CASCADE
    )

    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user.username} - {self.product.name}"    
    
class Cart(models.Model):

    product = models.ForeignKey(
        Product,
        on_delete=models.CASCADE
    )

    quantity = models.IntegerField(default=1)

    def __str__(self):
        return self.product.name

    class Meta:
        verbose_name = "Cart"
        verbose_name_plural = "Cart"

class Order(models.Model):

    customer_name = models.CharField(max_length=100)

    phone = models.CharField(max_length=15)

    address = models.TextField()

    total_amount = models.IntegerField()

    STATUS_CHOICES = [

    ("Placed","Placed"),
    ("Packed","Packed"),
    ("Shipped","Shipped"),
    ("Delivered","Delivered"),
    ("Cancelled","Cancelled"),

    ]

    status = models.CharField(
    max_length=20,
    choices=STATUS_CHOICES,
    default="Placed"
    )
    is_cancelled = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.customer_name
class OrderItem(models.Model):

    order = models.ForeignKey(
        Order,
        on_delete=models.CASCADE
    )

    product = models.ForeignKey(
        Product,
        on_delete=models.CASCADE
    )

    quantity = models.IntegerField()

    price = models.IntegerField()

    def __str__(self):
        return self.product.name    
from django.contrib.auth.models import User

class ChatUsage(models.Model):

    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE
    )

    date = models.DateField(auto_now_add=True)

    count = models.IntegerField(default=0)

    def __str__(self):
        return f"{self.user.username} - {self.date}"    