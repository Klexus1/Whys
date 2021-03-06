from django.contrib import admin

from core.models import *

@admin.register(Catalog)
class CatalogAdmin(admin.ModelAdmin):
    list_display = (
        "id",
        "nazev",
    )
    list_display_links =(
        "id",
        "nazev",
    )
    fields = (
        "id",
        "nazev",
        "obrazek_id",
        "products_ids",
        "attributes_ids",
    )
    list_filter = (
        "obrazek_id",
        "products_ids",
        "attributes_ids",
    )