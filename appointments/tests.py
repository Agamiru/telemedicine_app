import datetime
import json

from django.test import TestCase
from django.test import Client
from django.core.exceptions import ValidationError
from django.contrib.auth import get_user_model

from doctors.models import Doctor
from patients.models import Patient

# Create your tests here.


class TestViews(TestCase):

    def setUp(self) -> None:
        self.client = Client()
        now = datetime.datetime.now()
        time_delta_1 = datetime.timedelta(days=3)
        time_delta_2 = datetime.timedelta(days=3, hours=5)
        start = now + time_delta_1
        end = now + time_delta_2
        apptmnt_data = {
            "start_time": str(start), "end_time": str(end),
        }
        self.data = apptmnt_data
        # Doc and Patient user instances
        user_model = get_user_model()
        self.doc_user_inst, _ = user_model.objects.get_or_create(
            email="loki@ymail.com", password="chidi007", is_doctor=True
        )
        self.patient_user_inst, _ = user_model.objects.get_or_create(
            email="yaml@gmail.com", password="chidi007", is_doctor=False
        )

    def test_view(self):
        # Test creating Unavailable times
        doc_data = {
            "first_name": "Loki", "last_name": "Nnadi",
            "age": 46, "gender": "M", "user": self.doc_user_inst
        }
        doc_inst, _ = Doctor.objects.get_or_create(**doc_data)

        unav_start = datetime.datetime.now() + datetime.timedelta(days=3)
        unav_end = datetime.datetime.now() + datetime.timedelta(days=3, hours=3)

        unav_kwargs = {
            "start_time": str(unav_start), "end_time": str(unav_end),
            "doctor": doc_inst.id
        }
        response = self.client.post(
            f"/create/appointment/unavailable/{self.doc_user_inst.id}/", unav_kwargs
        )
        self.assertEqual(response.status_code, 200)

        # Test creating appointment with overlapping times
        patnt_data = {
            "first_name": "Shade", "last_name": "Kuti",
            "age": 23, "gender": "F", "user": self.patient_user_inst
        }
        patnt_inst, _ = Patient.objects.get_or_create(**patnt_data)

        appmnt_start = datetime.datetime.now() + datetime.timedelta(days=3)
        appmnt_end = datetime.datetime.now() + datetime.timedelta(days=3, hours=2)

        appmnt_kwargs = {
            "start_time": str(appmnt_start), "end_time": str(appmnt_end),
            "doctor": doc_inst.id, "patient": patnt_inst.id
        }

        response = self.client.post(
            f"/create/appointment/{self.patient_user_inst.id}/", appmnt_kwargs
        )
        self.assertEqual(response.status_code, 400)

        # Test creating appointment with non overlapping times
        appmnt_start = datetime.datetime.now() + datetime.timedelta(days=4)
        appmnt_end = datetime.datetime.now() + datetime.timedelta(days=4, hours=2, minutes=47)

        appmnt_kwargs = {
            "start_time": str(appmnt_start), "end_time": str(appmnt_end),
            "doctor": doc_inst.id, "patient": patnt_inst.id
        }
        response = self.client.post(
            f"/create/appointment/{self.patient_user_inst.id}/", appmnt_kwargs
        )
        self.assertEqual(response.status_code, 200)

        # Test future time
        appmnt_start = datetime.datetime(2020, 11, 2)
        appmnt_end = datetime.datetime.now() + datetime.timedelta(days=4, hours=3)

        appmnt_kwargs = {
            "start_time": str(appmnt_start), "end_time": str(appmnt_end),
            "doctor": doc_inst.id, "patient": patnt_inst.id
        }
        response = self.client.post(
            f"/create/appointment/{self.patient_user_inst.id}/", appmnt_kwargs
        )
        self.assertEqual(response.status_code, 400)

        # Test positive duration
        appmnt_start = datetime.datetime.now() + datetime.timedelta(days=4)
        appmnt_end = datetime.datetime.now()

        appmnt_kwargs = {
            "start_time": str(appmnt_start), "end_time": str(appmnt_end),
            "doctor": doc_inst.id, "patient": patnt_inst.id
        }
        response = self.client.post(
            f"/create/appointment/{self.patient_user_inst.id}/", appmnt_kwargs
        )
        self.assertEqual(response.status_code, 400)


