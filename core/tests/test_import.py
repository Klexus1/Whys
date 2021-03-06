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


class TestImportFKAndM2M(APITestCase):
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
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
