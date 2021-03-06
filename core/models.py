from django.db import models


class AttributeName(models.Model):
    id = models.PositiveIntegerField(unique=True, db_index=True, primary_key=True)
    nazev = models.CharField(max_length=100)
    kod = models.CharField(blank=True, max_length=100)
    zobrazit = models.BooleanField(blank=True, null=True)

    def __str__(self):
        return self.nazev

class AttributeValue(models.Model):
    id = models.PositiveIntegerField(unique=True, db_index=True, primary_key=True)
    hodnota = models.CharField(max_length=100)


    def __str__(self):
        return self.hodnota

class Attribute(models.Model):
    id = models.PositiveIntegerField(unique=True, db_index=True, primary_key=True)
    nazev_atributu_id = models.ForeignKey(AttributeName, on_delete=models.DO_NOTHING, related_name="attrstoname")
    hodnota_atributu_id = models.ForeignKey(AttributeValue, on_delete=models.DO_NOTHING, related_name="attrstovalue")



class Product(models.Model):
    id = models.PositiveIntegerField(unique=True, db_index=True, primary_key=True)
    nazev = models.CharField(max_length=200, blank=True, null=True)
    description = models.TextField(blank=True, null=True)
    cena = models.CharField(max_length=50)
    mena = models.CharField(max_length=5, blank=True, null=True)
    published_on = models.DateTimeField(blank=True, null=True)
    is_published = models.BooleanField(blank=True, null=True)

    def __str__(self):
        if self.nazev:
            return self.nazev
        return str(self.id)


class Image(models.Model):
    id = models.PositiveIntegerField(unique=True, db_index=True, primary_key=True)
    obrazek = models.URLField()
    nazev = models.CharField(blank=True, max_length=50)

    def __str__(self):
        if self.nazev:
            return self.nazev
        return str(self.id)


class ProductImage(models.Model):
    id = models.PositiveIntegerField(unique=True, db_index=True, primary_key=True)
    product = models.ForeignKey(Product, on_delete=models.DO_NOTHING)
    obrazek_id = models.ForeignKey(Image, on_delete=models.DO_NOTHING)
    nazev = models.CharField(max_length=70)

    def __str__(self):
        return self.nazev



class ProductAttributes(models.Model):
    id = models.PositiveIntegerField(unique=True, db_index=True, primary_key=True)
    product = models.ForeignKey(Product, on_delete=models.DO_NOTHING)
    attribute = models.ForeignKey(Attribute, on_delete=models.DO_NOTHING)


class Catalog(models.Model):
    id = models.PositiveIntegerField(unique=True, db_index=True, primary_key=True)
    nazev = models.CharField(max_length=70, blank=True, null=True)
    obrazek_id = models.ForeignKey(Image, on_delete=models.DO_NOTHING, blank=True, null=True)
    products_ids = models.ManyToManyField(Product)
    attributes_ids = models.ManyToManyField(Attribute)

    def __str__(self):
        if self.nazev:
            return self.nazev
        return str(self.id)

