from django.db import models
from django.contrib.auth.models import User
from product.models import Product

# Order status choices
class OrderStatus(models.TextChoices):
    PROCESSING = 'Processing'
    SHIPPED = 'Shipped'
    DELIVERED = 'Delivered'

# Payment status choices
class PaymentStatus(models.TextChoices):
    PAID = 'Paid'
    UNPAID = 'Unpaid'

# Payment mode choices
class PaymentMode(models.TextChoices):
    COD = 'COD'
    CARD = 'CARD'

# Order model
class Order(models.Model):
    city = models.CharField(max_length=100, default="", blank=False)
    zip_code = models.CharField(max_length=100, default="", blank=False)
    street = models.CharField(max_length=100, default="", blank=False)
    state = models.CharField(max_length=100, default="", blank=False)
    country = models.CharField(max_length=100, default="", blank=False)
    phone_no = models.CharField(max_length=100, default="", blank=False)
    total_amount = models.IntegerField(blank=False)
    payment_status = models.CharField(max_length=30, choices=PaymentStatus.choices, default=PaymentStatus.UNPAID)
    payment_mode = models.CharField(max_length=30, choices=PaymentMode.choices, default=PaymentMode.COD)
    status = models.CharField(max_length=30, choices=OrderStatus.choices, default=OrderStatus.PROCESSING)
    user = models.ForeignKey(User, null=True, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return str(self.id)

# OrderItem model
class OrderItem(models.Model):
    product = models.ForeignKey(Product, null=True, blank=False, on_delete=models.SET_NULL)
    order = models.ForeignKey(Order, blank=False, on_delete=models.CASCADE, related_name='orderitems')
    name = models.CharField(max_length=100, default="", blank=False)
    quantity = models.IntegerField(default=1, blank=False)
    price = models.DecimalField(max_digits=7, decimal_places=2, blank=False)

    def __str__(self):
        return self.name
