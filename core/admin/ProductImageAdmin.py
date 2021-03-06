from django.contrib import admin

from core.models import *

@admin.register(ProductImage)
class ProductImageAdmin(admin.ModelAdmin):
    list_display = (
        "id",
        "product",
        "obrazek_id",
        "nazev",

    )
    list_display_links =(
        "id",
        "nazev",
    )
    fields = (
        "id",
        "product",
        "obrazek_id",
        "nazev",
    )
    list_filter = (
        "product",
        "obrazek_id",
    )