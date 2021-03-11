from django.db import models
from django.core.exceptions import ValidationError

from registration.models import User

# Create your models here.


class Patient(models.Model):
    gender_choices = (
        ("Male", "Male"),
        ("Female", "Female"),
        ("Other", "Other")
    )
    user = models.OneToOneField(
        User, on_delete=models.CASCADE, related_name="patient"
    )
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    other_names = models.CharField(max_length=100, blank=True)
    age = models.IntegerField()
    gender = models.CharField(max_length=10, choices=gender_choices, blank=False)
    emr = models.JSONField(default=dict)

    def save(self, *args, **kwargs):
        if self.user.is_doctor:
            raise ValidationError("User must be a patient to have a patients profile")

        super().save(*args, **kwargs)
