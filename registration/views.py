from rest_framework.views import APIView
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework import status

from .serializers import UserSerializer

# Create your views here.


class RegisterUser(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        password = request.data.get("password")
        serializer = UserSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save(password=password)
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

# Create your views here.
