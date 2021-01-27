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


class CreateAppointment(APIView):
    # permission_classes = [IsAuthenticated]
    # authentication_classes = [CustomSessionAuthentication]

    def post(self, request, user_id):
        if self.verify_user(user_id):
            serializer = AppointmentSerializer(data=request.data)
            if serializer.is_valid():
                is_valid_or_err = self.form_valid_or_err(serializer.validated_data)
                if is_valid_or_err[0]:
                    serializer.save()
                    return Response(serializer.data, status=status.HTTP_200_OK)
                err = is_valid_or_err[1]
                return Response(err, status=status.HTTP_400_BAD_REQUEST)
            else:
                return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        message = {"message": f"User with id '{request.user.id}' is not a patient"}
        return Response(data=message, status=status.HTTP_401_UNAUTHORIZED)

    def form_valid_or_err(self, data: dict) -> Union[Tuple[bool, None], Tuple[bool, err]]:
        data = dict(data)
        print(f"data: {data}")
        form = AppointmentForm(data)
        try:
            form.save()
            return True, None
        except ValueError:
            return False, form.errors.as_data()


    @staticmethod
    def verify_user(user_id) -> bool:
        user_model = get_user_model()
        try:
            user = user_model.objects.get(id=user_id, is_doctor=False)
            if user:
                return True
        except doesnt_exist:
            return False
        return False


class CreateUnavailable(APIView):
    # permission_classes = [IsAuthenticated]
    # authentication_classes = [CustomSessionAuthentication]

    def post(self, request, user_id):
        if self.verify_user(user_id):
            serializer = UnavailableSerializer(data=request.data)
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data, status=status.HTTP_200_OK)
            else:
                return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        message = {"message": f"User with id '{user_id}' is not a Doctor"}
        return Response(data=message, status=status.HTTP_401_UNAUTHORIZED)

    @staticmethod
    def verify_user(user_id) -> bool:
        user_model = get_user_model()
        try:
            user = user_model.objects.get(id=user_id, is_doctor=True)
            if user:
                return True
        except doesnt_exist:
            return False
        return False
