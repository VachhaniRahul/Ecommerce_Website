from django.contrib import admin
from .models import Product, Category, ProductImage, ColorVariant, SizeVariant, Coupon


admin.site.register(Category)

class ProductImageAdmin(admin.StackedInline):
    model = ProductImage

class ProductAdmin(admin.ModelAdmin):
    list_display = ['product_name', 'price', 'category']
    inlines = [ProductImageAdmin]

class ColorVariantAdmin(admin.ModelAdmin):
    list_display = ['color_name', 'price']
    model = ColorVariant

class SizeVariantAdmin(admin.ModelAdmin):
    list_display = ['size_name', 'price']
    model = SizeVariant

class CouponAdmin(admin.ModelAdmin):
    list_display = ['coupon_code', 'is_expired', 'discount_price']
    model = Coupon

admin.site.register(Product, ProductAdmin)
admin.site.register(ProductImage)
admin.site.register(ColorVariant, ColorVariantAdmin)
admin.site.register(SizeVariant, SizeVariantAdmin)
admin.site.register(Coupon, CouponAdmin)
