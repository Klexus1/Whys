"""whystest URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from core.views import swagger as swagger_views
from core.views import general as general_views
from core.views import import_prods as import_prods_views
from rest_framework import routers

from rest_framework_swagger.views import get_swagger_view

schema_view = get_swagger_view(title='Pastebin API')


router = routers.DefaultRouter()
router.register(r'product', general_views.ProductListViewSet, basename="Product")
router.register(r'attributeName', general_views.AttributeNameViewSet, basename="AttributeName")
router.register(r'attributeValue', general_views.AttributeValueViewSet, basename="AttributeValue")
router.register(r'attribute', general_views.AttributeViewSet, basename="Attribute")
router.register(r'productImage', general_views.ProductImageViewSet, basename="ProductImage")
router.register(r'image', general_views.ImageViewSet, basename="Image")
router.register(r'productAttributes', general_views.ProductAttributesViewSet, basename="ProductAttributes")
router.register(r'catalogViewSet', general_views.CatalogViewSet, basename="Catalog")
router.register(r'product', general_views.ProductListViewSet, basename="product")


urlpatterns = [
    path('admin/', admin.site.urls),
    path('accounts/', include('rest_framework.urls')),
    path('swagger/', swagger_views.SwaggerSchemaView.as_view()),
    path('detail/', include((router.urls, 'core'), namespace='detail')),
    path('import/', import_prods_views.ImportDataView.as_view(), name='import'),
]
