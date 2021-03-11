from typing import Union, TypeVar, Tuple

from django.contrib.auth import get_user_model
from django.db.models import ObjectDoesNotExist as doesnt_exist

from rest_framework.views import APIView
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework import status

from .serializers import PatientSerializer


# types
err_msg = TypeVar("err_msg", bound=str)


class RegisterPatient(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        is_patient = self.is_patient(request)
        if is_patient[0]:
            data = request.data.copy()
            # Title case gender
            gender = data.get("gender")
            if gender is not None:
                data["gender"] = gender.title()
            serializer = PatientSerializer(data=data)
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data, status=status.HTTP_200_OK)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        else:
            return Response({"unauthorized": is_patient[1]}, status=status.HTTP_401_UNAUTHORIZED)

    def is_patient(self, request) -> Union[Tuple[bool, None], Tuple[bool, err_msg]]:
        err_message_1 = "Only patients are allowed to create a patients profile"
        err_message_2 = "This user doesnt exist"
        user_model = get_user_model()
        user_id = request.data.get("user")
        try:
            user_inst = user_model.objects.get(id=user_id)
            return (True, None) if not user_inst.is_doctor else (False, err_message_1)
        except doesnt_exist:
            return False, err_message_2


