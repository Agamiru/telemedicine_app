from rest_framework import serializers

from .models import Doctor


class DoctorSerializer(serializers.ModelSerializer):

    class Meta:
        model = Doctor
        fields = [
            "id", "user", "first_name", "last_name", "gender", "age"
        ]
