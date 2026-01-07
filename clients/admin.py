from django.contrib import admin
from .models import Client, ClientImage, ClientDescriptionPoint


class ClientImageInline(admin.TabularInline):
    model = ClientImage
    extra = 1


class ClientDescriptionInline(admin.TabularInline):
    model = ClientDescriptionPoint
    extra = 1


@admin.register(Client)
class ClientAdmin(admin.ModelAdmin):
    list_display = ("title", "category", "status")
    prepopulated_fields = {"slug": ("title",)}
    inlines = [
        ClientImageInline,        # carousel images
        ClientDescriptionInline,  # description bullet points
    ]
