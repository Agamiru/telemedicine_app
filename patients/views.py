from django.shortcuts import render

# Create your views here.

from rest_framework.views import APIView
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework import status

from .serializers import PatientSerializer

# Create your views here.


class RegisterPatient(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        serializer = PatientSerializer(data=request.data)
        if serializer.is_valid():
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


