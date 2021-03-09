from rest_framework.test import APITestCase
from rest_framework import status
from rest_framework.authtoken.models import Token
from rest_framework.test import APIRequestFactory
from rest_framework.test import force_authenticate
from userprofile.models import User
from core.models import *


class TestImportNoFK(APITestCase):
    """
    Test for importing data for models with no FKs
    """
    def setUp(self):
        self.factory = APIRequestFactory()
        self.user = User.objects.create_user(
            username='user@foo.com', email='user@foo.com', password='top_secret')
        self.token = Token.objects.create(user=self.user)
        self.token.save()

    def test_importing_prods(self):
        """Testing creation"""
        data = [
            {
                "AttributeName": {
                    "id": 1,
                    "nazev": "Barva"
                }
            },
            {
                "AttributeValue": {
                    "id": 1,
                    "hodnota": "modrá"
                }
            }
        ]
        response = self.client.post("/import/", data, format="json", HTTP_AUTHORIZATION='Token {}'.format(self.token))
        force_authenticate(response, user=self.user)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)


class TestImportFK(APITestCase):
    """
    Test for importing data for models with FKs
    """

    def setUp(self):
        self.factory = APIRequestFactory()
        self.user = User.objects.create_user(
            username='user@foo.com', email='user@foo.com', password='top_secret')
        self.token = Token.objects.create(user=self.user)
        self.token.save()

    def test_importing_prods(self):
        """Testing FKs creation"""
        data = [
            {
                "AttributeName": {
                    "id": 1,
                    "nazev": "Barva"
                }
            },
            {
                "AttributeValue": {
                    "id": 1,
                    "hodnota": "modrá"
                }
            },
            {
                "Attribute": {
                    "id": 1,
                    "nazev_atributu_id": 1,
                    "hodnota_atributu_id": 1
                }
            }

        ]
        response = self.client.post("/import/", data, format="json", HTTP_AUTHORIZATION='Token {}'.format(self.token))
        force_authenticate(response, user=self.user)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)


class TestInvalidImportM2M(APITestCase):

    def setUp(self):
        self.factory = APIRequestFactory()
        self.user = User.objects.create_user(
            username='user@foo.com', email='user@foo.com', password='top_secret')
        self.token = Token.objects.create(user=self.user)
        self.token.save()

    def test_importing_prods(self):
        """testing missing data (attributes_ids) with Catalog"""
        data = [
            {
                "Product": {
                    "id": 2,
                    "cena": "900"
                }
            },
            {
                "Product": {
                    "id": 5,
                    "nazev": "Funko Pop God of War Kratos",
                    "description": "Kratos, otec Atrea, se dočkal své vinylové POP! figurky od společnosti Funko.",
                    "cena": "800",
                    "mena": "CZK",
                    "is_published": 'true'
                }
            },
            {
                "Catalog": {
                    "id": 1,
                    "products_ids": [
                        2,
                        5
                    ]
                }
            }

        ]
        response = self.client.post("/import/", data, format="json", HTTP_AUTHORIZATION='Token {}'.format(self.token))
        force_authenticate(response, user=self.user)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)


class TestValidImportFKAndM2M(APITestCase):

    def setUp(self):
        self.factory = APIRequestFactory()
        self.user = User.objects.create_user(
            username='user@foo.com', email='user@foo.com', password='top_secret')
        self.token = Token.objects.create(user=self.user)
        self.token.save()

    def test_importing_prods(self):
        """testing missing data (attributes_ids) with Catalog"""
        data = [
            {
                "Product": {
                    "id": 2,
                    "cena": "900"
                }
            },
            {
                "Image": {
                    "id": 4,
                    "obrazek": "https://free-images.com/lg/7687/blue_jay_bird_nature.jpg"
                }
            },
            {
                "Product": {
                    "id": 5,
                    "nazev": "Funko Pop God of War Kratos",
                    "description": "Kratos, otec Atrea, se dočkal své vinylové POP! figurky od společnosti Funko.",
                    "cena": "800",
                    "mena": "CZK",
                    "is_published": 'true'
                }
            },
            {
                "AttributeName": {
                    "id": 5,
                    "nazev": "Skladem"
                }
            },
            {
                "AttributeValue": {
                    "id": 8,
                    "hodnota": "světle modrá"
                }
            },
            {
                "Attribute": {
                    "id": 2,
                    "nazev_atributu_id": 5,
                    "hodnota_atributu_id": 8
                }
            },
            {
                "Catalog": {
                    "id": 1,
                    "nazev": "Výprodej 2018",
                    "obrazek_id": 4,
                    "products_ids": [
                        5
                    ],
                    "attributes_ids": [
                        2
                    ]
                }
            }

        ]
        response = self.client.post("/import/", data, format="json", HTTP_AUTHORIZATION='Token {}'.format(self.token))
        force_authenticate(response, user=self.user)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)


class TestUnorderedImport(APITestCase):

    def setUp(self):
        self.factory = APIRequestFactory()
        self.user = User.objects.create_user(
            username='user@foo.com', email='user@foo.com', password='top_secret')
        self.token = Token.objects.create(user=self.user)
        self.token.save()

    def test_importing_prods(self):
        """testing unordered data (referencing ids that do not yet exist - handled by iterations later)"""
        data = [
            {
                "Catalog": {
                    "id": 1,
                    "nazev": "Výprodej 2018",
                    "obrazek_id": 4,
                    "products_ids": [
                        5
                    ],
                    "attributes_ids": [
                        2
                    ]
                }
            },

            {
                "Product": {
                    "id": 2,
                    "cena": "900"
                }
            },
            {
                "Image": {
                    "id": 4,
                    "obrazek": "https://free-images.com/lg/7687/blue_jay_bird_nature.jpg"
                }
            },
            {
                "Product": {
                    "id": 5,
                    "nazev": "Funko Pop God of War Kratos",
                    "description": "Kratos, otec Atrea, se dočkal své vinylové POP! figurky od společnosti Funko.",
                    "cena": "800",
                    "mena": "CZK",
                    "is_published": 'true'
                }
            },
            {
                "AttributeName": {
                    "id": 5,
                    "nazev": "Skladem"
                }
            },
            {
                "AttributeValue": {
                    "id": 8,
                    "hodnota": "světle modrá"
                }
            },
            {
                "Attribute": {
                    "id": 2,
                    "nazev_atributu_id": 5,
                    "hodnota_atributu_id": 8
                }
            },

        ]
        response = self.client.post("/import/", data, format="json", HTTP_AUTHORIZATION='Token {}'.format(self.token))
        force_authenticate(response, user=self.user)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)


class TestUpdateImport(APITestCase):

    def setUp(self):
        self.factory = APIRequestFactory()
        self.user = User.objects.create_user(
            username='user@foo.com', email='user@foo.com', password='top_secret')
        self.token = Token.objects.create(user=self.user)
        self.token.save()

    def test_importing_prods(self):
        """testing unordered data where update (patch) is applied"""
        data = [
            {
                "Product": {
                    "id": 1,
                    "cena": "900"
                }
            },
            {
                "Product": {
                    "id": 1,
                    "cena": "800"
                }
            },
        ]
        response = self.client.post("/import/", data, format="json", HTTP_AUTHORIZATION='Token {}'.format(self.token))
        force_authenticate(response, user=self.user)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        product = Product.objects.get(id=1)
        self.assertEqual(product.cena, "800")


class TestM2MUpdateImport(APITestCase):

    def setUp(self):
        self.factory = APIRequestFactory()
        self.user = User.objects.create_user(
            username='user@foo.com', email='user@foo.com', password='top_secret')
        self.token = Token.objects.create(user=self.user)
        self.token.save()

    def test_importing_prods(self):
        """testing unordered data where update (patch) on m2m field is applied"""
        data = [
            {
                "Product": {
                    "id": 2,
                    "cena": "900"
                }
            },
            {
                "Image": {
                    "id": 4,
                    "obrazek": "https://free-images.com/lg/7687/blue_jay_bird_nature.jpg"
                }
            },
            {
                "Product": {
                    "id": 5,
                    "nazev": "Funko Pop God of War Kratos",
                    "description": "Kratos, otec Atrea, se dočkal své vinylové POP! figurky od společnosti Funko.",
                    "cena": "800",
                    "mena": "CZK",
                    "is_published": 'true'
                }
            },
            {
                "Product": {
                    "id": 6,
                    "nazev": "Test Prod",
                    "cena": "800"
                }
            },
            {
                "AttributeName": {
                    "id": 5,
                    "nazev": "Skladem"
                }
            },
            {
                "AttributeValue": {
                    "id": 8,
                    "hodnota": "světle modrá"
                }
            },
            {
                "Attribute": {
                    "id": 2,
                    "nazev_atributu_id": 5,
                    "hodnota_atributu_id": 8
                }
            },
            {
                "Catalog": {
                    "id": 1,
                    "nazev": "Výprodej 2018",
                    "obrazek_id": 4,
                    "products_ids": [
                        5
                    ],
                    "attributes_ids": [
                        2
                    ]
                }
            },
            {
                "Catalog": {
                    "id": 1,
                    "nazev": "Výprodej 2018",
                    "obrazek_id": 4,
                    "products_ids": [
                        5,
                        6
                    ],
                    "attributes_ids": [
                        2
                    ]
                }
            },
        ]
        response = self.client.post("/import/", data, format="json", HTTP_AUTHORIZATION='Token {}'.format(self.token))
        force_authenticate(response, user=self.user)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        # catalog = Catalog.objects.get(id=1)
        self.assertEqual(Catalog.objects.filter(products_ids__id=5).exists(), True)
        self.assertEqual(Catalog.objects.filter(products_ids__id=6).exists(), True)
        self.assertEqual(Catalog.objects.filter(attributes_ids__id=2).exists(), True)
