from rest_framework import mixins, viewsets, status
from core.serializers import *
from core.models import *
from rest_framework.permissions import IsAuthenticated, AllowAny


class ProductListViewSet(
    mixins.RetrieveModelMixin,
    mixins.ListModelMixin,
    viewsets.GenericViewSet
):
    """
    Api endpoint that allows products to be created
    """
    serializer_class = ProductSerializer
    permission_classes = (AllowAny,)

    def get_queryset(self):
        return Product.objects.all()


class AttributeNameViewSet(
    mixins.RetrieveModelMixin,
    mixins.ListModelMixin,
    viewsets.GenericViewSet
):
    """
    Api endpoint that allows products to be created
    """
    serializer_class = AttributeNameSerializer
    permission_classes = (AllowAny,)

    def get_queryset(self):
        return AttributeName.objects.all()


class AttributeValueViewSet(
    mixins.RetrieveModelMixin,
    mixins.ListModelMixin,
    viewsets.GenericViewSet
):
    """
    Api endpoint that allows products to be created
    """
    serializer_class = AttributeValueSerializer
    permission_classes = (AllowAny,)

    def get_queryset(self):
        return AttributeValue.objects.all()


class AttributeViewSet(
    mixins.RetrieveModelMixin,
    mixins.ListModelMixin,
    viewsets.GenericViewSet
):
    """
    Api endpoint that allows products to be created
    """
    serializer_class = AttributeSerializer
    permission_classes = (AllowAny,)

    def get_queryset(self):
        return Attribute.objects.all()


class ImageViewSet(
    mixins.RetrieveModelMixin,
    mixins.ListModelMixin,
    viewsets.GenericViewSet
):
    """
    Api endpoint that allows products to be created
    """
    serializer_class = ImageSerializer
    permission_classes = (AllowAny,)

    def get_queryset(self):
        return Image.objects.all()


class ProductImageViewSet(
    mixins.RetrieveModelMixin,
    mixins.ListModelMixin,
    viewsets.GenericViewSet
):
    """
    Api endpoint that allows products to be created
    """
    serializer_class = ProductSerializer
    permission_classes = (AllowAny,)

    def get_queryset(self):
        return ProductImage.objects.all()


class ProductAttributesViewSet(
    mixins.RetrieveModelMixin,
    mixins.ListModelMixin,
    viewsets.GenericViewSet
):
    """
    Api endpoint that allows products to be created
    """
    serializer_class = ProductAttributesSerializer
    permission_classes = (AllowAny,)

    def get_queryset(self):
        return ProductAttributes.objects.all()


class CatalogViewSet(
    mixins.RetrieveModelMixin,
    mixins.ListModelMixin,
    viewsets.GenericViewSet
):
    """
    Api endpoint that allows products to be created
    """
    serializer_class = CatalogSerializer
    permission_classes = (AllowAny,)

    def get_queryset(self):
        return Catalog.objects.all()

