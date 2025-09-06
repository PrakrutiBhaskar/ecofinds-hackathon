from django.contrib import admin
from .models import Profile, Product, CartItem, Purchase

admin.site.register(Profile)
admin.site.register(Product)
admin.site.register(CartItem)
admin.site.register(Purchase)
