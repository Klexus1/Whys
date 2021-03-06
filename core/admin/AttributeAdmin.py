from django.contrib import admin

from core.models import *

@admin.register(Attribute)
class AttributeAdmin(admin.ModelAdmin):
    list_display = (
        "id",
        "nazev_atributu_id",
        "hodnota_atributu_id",
    )
    list_display_links =(
        "id",
    )
    fields = (
        "id",
        "nazev_atributu_id",
        "hodnota_atributu_id",
    )
    list_filter = (
        "nazev_atributu_id",
        "hodnota_atributu_id",
    )