from django.contrib import admin
from .models import Profile, Cart, CartItems, Invoice

@admin.register(Cart)
class CartAdmin(admin.ModelAdmin):
    list_display = ['user', 'is_paid']
    model = Cart

@admin.register(CartItems)
class CartItemsAdmin(admin.ModelAdmin):
    list_display = ['cart', 'product']

@admin.register(Invoice)
class CartItemsAdmin(admin.ModelAdmin):
    list_display = ['email', 'file']

admin.site.register(Profile)

