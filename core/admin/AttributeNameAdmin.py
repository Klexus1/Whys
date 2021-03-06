from django.contrib import admin

from core.models import *

@admin.register(AttributeName)
class AttributeNameAdmin(admin.ModelAdmin):
    list_display = (
        "id",
        "nazev",
        "kod",
        "zobrazit",
    )
    list_display_links =(
        "id",
        "nazev",
    )
    fields = (
        "id",
        "nazev",
        "kod",
        "zobrazit",
    )
    list_filter = (
        "zobrazit",
    )