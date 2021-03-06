from django.contrib import admin

from core.models import *

@admin.register(AttributeValue)
class AttributeValueAdmin(admin.ModelAdmin):
    list_display = (
        "id",
        "hodnota",

    )
    list_display_links =(
        "id",
        "hodnota",
    )
    fields = (
        "id",
        "hodnota",
    )
    list_filter = (
        "hodnota",
    )