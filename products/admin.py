from django.contrib import admin
from .models import Product, ProductImage, ProductDescriptionPoint


class ProductImageInline(admin.TabularInline):
    model = ProductImage
    extra = 1


class ProductDescriptionInline(admin.TabularInline):
    model = ProductDescriptionPoint
    extra = 1


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ("title", "category", "status")
    prepopulated_fields = {"slug": ("title",)}
    inlines = [
        ProductImageInline,        # carousel images
        ProductDescriptionInline,  # description bullet points
    ]
