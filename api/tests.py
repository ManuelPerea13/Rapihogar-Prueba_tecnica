import json
from rapihogar.models import User, Pedido, Technical, Scheme
from django.urls import reverse

from rest_framework.authtoken.models import Token
from rest_framework.test import APITestCase
from rapihogar.models import Company


class CompanyListCreateAPIViewTestCase(APITestCase):
    url = reverse("company-list")

    def setUp(self):
        self.username = "user_test"
        self.email = "test@rapihigar.com"
        self.password = "Rapi123"
        self.user = User.objects.create_user(self.username, self.email, self.password)
        self.technical = Technical.objects.create(full_name="technical test")
        self.scheme = Scheme.objects.create(name="scheme test")
        self.token = Token.objects.create(user=self.user)
        self.api_authentication()

    def api_authentication(self):
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.token.key)

    def test_create_company(self):
        response = self.client.post(self.url,
                                    {
                                        "name": "company delete!",
                                        "phone": "123456789",
                                        "email": "test@rapihigar.com",
                                        "website": "http://www.rapitest.com"
                                    }
                                    )
        self.assertEqual(201, response.status_code)

    def test_list_company(self):
        response = self.client.get(self.url)
        self.assertEqual(200, response.status_code)
        self.assertTrue(len(json.loads(response.content)) == Company.objects.count())

    def test_pedido_creation(self):
        pedido = Pedido.objects.create(
            client=self.user,
            technical=self.technical,
            hours_worked=5,
            scheme=self.scheme,
            type_request=Pedido.PEDIDO,
        )

        self.assertEqual(pedido.client, self.user)
        self.assertEqual(pedido.technical, self.technical)
        self.assertEqual(pedido.hours_worked, 5)
        self.assertEqual(pedido.scheme, self.scheme)
        self.assertEqual(pedido.type_request, Pedido.PEDIDO)
