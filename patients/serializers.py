from rest_framework import serializers

from .models import Patient


class PatientSerializer(serializers.ModelSerializer):

    class Meta:
        model = Patient
        fields = [
            "id", "user", "first_name", "last_name", "gender", "age"
        ]
