from django.test import TestCase
from django.test import Client
from django.core.exceptions import ValidationError
from django.contrib.auth import get_user_model

from .models import Doctor

# Create your tests here.


class TestViews(TestCase):

    def setUp(self) -> None:
        self.client = Client()
        doc_data = {
            "first_name": "Chidi", "last_name": "Nnadi",
            "age": 46, "gender": "M"
        }
        self.data = doc_data

    def test_view(self):
        user_model = get_user_model()
        user_inst, _ = user_model.objects.get_or_create(
            email="Chidi@ymail.com", password="chidi007",
            is_doctor=True
        )
        self.data["user"] = user_inst.id
        response = self.client.post("/register/doctor/", self.data)
        self.assertEqual(response.status_code, 200)
        # Check with incorrect details
        new_data = self.data.copy()
        new_data.pop("last_name")
        response = self.client.post("/register/doctor/", new_data)
        self.assertEqual(response.status_code, 400)

        # Test unauthorized user
        user_inst, _ = user_model.objects.get_or_create(
            email="Chahk@ymail.com", password="chidi007",
            is_doctor=False
        )
        new_data = self.data.copy()
        new_data["user"] = user_inst.id
        response = self.client.post("/register/doctor/", new_data)
        self.assertEqual(response.status_code, 401)


class TestModel(TestCase):

    def setUp(self) -> None:
        self.client = Client()
        doc_data = {
            "first_name": "Nnaemeka", "last_name": "Nnadi",
            "age": 26, "gender": "M"
        }
        self.data = doc_data

    def test_model(self):
        user_model = get_user_model()
        user_inst, _ = user_model.objects.get_or_create(
            email="Chidi@bmail.com", password="chidi007",
            is_doctor=False
        )
        self.data["user"] = user_inst
        # Check that users who aren't doctors cannot create a doctors profile
        self.assertRaisesMessage(
            ValidationError,
            "User must be doctor to have a doctors profile",
            Doctor.objects.create, **self.data
        )


