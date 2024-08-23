from django.db import models
from django.contrib.auth.models import User

# Create your models here.
class Category(models.TextChoices):
    Computers='Computers'
    Food='Food'
    Cloths='Cloths'
    Kids='Kids'

   
class Product(models.Model): 
    name = models.CharField(max_length=25, default="", blank=False)
    description = models.TextField(max_length=100, default="")
    price = models.DecimalField(max_digits=7, decimal_places=2, default=0)  # max_digits and decimal_places defined
    brand = models.CharField(max_length=100, default="", blank=False)
    category = models.CharField(max_length=50, choices=Category.choices)
    rating = models.DecimalField(max_digits=10, decimal_places=2, default=0)  # Specify decimal_places
    stock = models.IntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)
    user = models.ForeignKey(User, null=True, on_delete=models.CASCADE)
    def __str__(self):
        return self.name
    

class Review(models.Model):  
    product = models.ForeignKey(Product, null=True, on_delete=models.CASCADE, related_name='reviews')
    user = models.ForeignKey(User, null=True, on_delete=models.SET_NULL)
    rating = models.IntegerField(default=0)
    comment = models.TextField(max_length=100, default="")
    created_at = models.DateTimeField(auto_now_add=True)
    def __str__(self):
        return self.comment