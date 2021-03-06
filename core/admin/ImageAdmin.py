from django.contrib import admin

from core.models import *

@admin.register(Image)
class ImageAdmin(admin.ModelAdmin):
    list_display = (
        "id",
        "obrazek",
        "nazev",
    )
    list_display_links =(
        "id",
        "nazev",
    )
    fields = (
        "id",
        "obrazek",
        "nazev",
    )
