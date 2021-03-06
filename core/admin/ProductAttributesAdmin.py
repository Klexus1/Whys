from django.contrib import admin

from core.models import *

@admin.register(ProductAttributes)
class ProductAttributesAdmin(admin.ModelAdmin):
    list_display = (
        "id",
        "product",
        "attribute",

    )
    list_display_links =(
        "id",
    )
    fields = (
        "id",
        "product",
        "attribute",
    )
    list_filter = (
        "product",
        "attribute",
    )