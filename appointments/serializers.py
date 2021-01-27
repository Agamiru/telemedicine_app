from rest_framework import serializers

from .models import Appointment, Unavailable


class AppointmentSerializer(serializers.ModelSerializer):

    class Meta:
        model = Appointment
        fields = "__all__"


class UnavailableSerializer(serializers.ModelSerializer):

    class Meta:
        model = Unavailable
        fields = "__all__"