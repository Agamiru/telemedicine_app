from typing import Tuple, Union, TypeVar

from django.contrib.auth import get_user_model
from django.db.models import ObjectDoesNotExist as doesnt_exist
from django.core.exceptions import ValidationError

from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework import status

from .serializers import AppointmentSerializer, UnavailableSerializer
from .forms import AppointmentForm, UnavailableForm

# Types
err = TypeVar("err", bound=Exception)


class AppointmentMixin:
    form = None
    serializer = None
    message = "User with id '{user_id}' is not a {user_type}"
    user_type: str = None

    def post(self, request, user_id):
        if self.verify_user(user_id):
            serializer = self.serializer(data=request.data)
            if serializer.is_valid():
                is_valid_or_err = self.form_valid_or_err(serializer.validated_data)
                if is_valid_or_err[0]:
                    serializer.save()
                    return Response(serializer.data, status=status.HTTP_200_OK)
                err = is_valid_or_err[1]
                return Response(err, status=status.HTTP_400_BAD_REQUEST)
            else:
                return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        message = self.message.format(user_id=user_id, user_type=self.user_type)
        return Response(data=message, status=status.HTTP_401_UNAUTHORIZED)

    def verify_user(self, user_id) -> bool:
        is_doctor = True if self.user_type == "Doctor" else False
        user_model = get_user_model()
        try:
            user = user_model.objects.get(id=user_id, is_doctor=is_doctor)
            if user:
                return True
        except doesnt_exist:
            return False
        return False

    def form_valid_or_err(self, data: dict) -> Union[Tuple[bool, None], Tuple[bool, err]]:
        data = dict(data)
        form = self.form(data)
        try:
            # No need to call is_valid for form after serializer validation
            form.save()
            return True, None
        except ValueError:
            return False, form.errors.as_data()


class CreateAppointment(APIView, AppointmentMixin):
    form = AppointmentForm
    serializer = AppointmentSerializer
    user_type = "Patient"


class CreateUnavailable(APIView, AppointmentMixin):
    form = UnavailableForm
    serializer = UnavailableSerializer
    user_type = "Doctor"
