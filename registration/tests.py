from django.test import TestCase
from django.test import Client

# Create your tests here.


class TestViews(TestCase):

    def setUp(self) -> None:
        self.client = Client()
        data = {
            "email": "chidi@gmail.com",
            "password": "chidi007"
        }
        self.data = data

    def test_view(self):
        response = self.client.post("/register/", self.data)
        self.assertEqual(response.status_code, 200)
        self.data["email"] = "chidi@gmail"
        response = self.client.post("/register/", self.data)
        self.assertEqual(response.status_code, 400)