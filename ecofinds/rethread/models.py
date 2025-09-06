# ecofinds/models.py

from django.db import models
from django.contrib.auth.models import User

CATEGORY_CHOICES = [
    ("electronics", "Electronics"),
    ("fashion", "Fashion"),
    ("furniture", "Furniture"),
    ("books", "Books"),
    ("other", "Other"),
]

class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    display_name = models.CharField(max_length=100, blank=True)

    def __str__(self):
        return self.display_name or self.user.username

class Product(models.Model):
    seller = models.ForeignKey(User, on_delete=models.CASCADE, related_name="products")
    title = models.CharField(max_length=200)
    description = models.TextField(blank=True)
    category = models.CharField(max_length=50, choices=CATEGORY_CHOICES)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    image = models.ImageField(upload_to="products/", blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["-created_at"]

    def __str__(self):
        return self.title

class CartItem(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="cart_items")
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1)
    added_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ("user", "product")

    def __str__(self):
        return f"{self.quantity} × {self.product.title}"

class Purchase(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="purchases")
    product = models.ForeignKey(Product, on_delete=models.SET_NULL, null=True)
    quantity = models.PositiveIntegerField(default=1)
    purchased_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.product} x{self.quantity} on {self.purchased_at:%Y-%m-%d}"
