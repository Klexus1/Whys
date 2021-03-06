from django.contrib import admin

from core.models import *

@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = (
        "id",
        "nazev",
        "cena",
        "mena",
        "published_on",
        "is_published",
    )
    list_display_links =(
        "id",
        "nazev",
    )
    fields = (
        "id",
        "nazev",
        "cena",
        "mena",
        "published_on",
        "is_published",
    )
    list_filter = (
        "cena",
        "mena",
        "is_published",
    )