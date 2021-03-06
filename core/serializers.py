from rest_framework.serializers import *
from .models import *


class AttributeNameSerializer(ModelSerializer):
    class Meta:
        model = AttributeName
        fields = (
            "id",
            "nazev",
            "kod",
            "zobrazit",
        )


class AttributeValueSerializer(ModelSerializer):
    class Meta:
        model = AttributeValue
        fields = (
            "id",
            "hodnota",
        )


class AttributeSerializer(ModelSerializer):
    class Meta:
        model = Attribute
        fields = (
            "id",
            "nazev_atributu_id",
            "hodnota_atributu_id",
        )


class ProductSerializer(ModelSerializer):
    class Meta:
        model = Product
        fields = (
            "id",
            "nazev",
            "description",
            "cena",
            "mena",
            "published_on",
            "is_published",
        )


class ProductImageSerializer(ModelSerializer):
    class Meta:
        model = ProductImage
        fields = (
            "id",
            "product",
            "obrazek_id",
            "nazev",
        )


class ProductAttributesSerializer(ModelSerializer):
    class Meta:
        model = ProductAttributes
        fields = (
            "id",
            "product",
            "attribute",
        )


class ImageSerializer(ModelSerializer):
    class Meta:
        model = Image
        fields = (
            "id",
            "obrazek",
            "nazev",
        )

class CatalogSerializer(ModelSerializer):
    products_ids = PrimaryKeyRelatedField(queryset=Product.objects.all(), many=True)
    attributes_ids = PrimaryKeyRelatedField(queryset=Attribute.objects.all(), many=True)
    class Meta:
        model = Catalog
        fields = (
            "id",
            "nazev",
            "obrazek_id",
            "products_ids",
            "attributes_ids",
        )

