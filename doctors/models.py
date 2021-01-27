from django.db import models
from django.core.exceptions import ValidationError

from registration.models import User

# Create your models here.


class Doctor(models.Model):
    gender_choices = (
        ("M", "Male"),
        ("F", "Female"),
    )
    user = models.OneToOneField(
        User, on_delete=models.CASCADE, related_name="doctor"
    )
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    other_names = models.CharField(max_length=100, blank=True)
    age = models.IntegerField()
    gender = models.CharField(max_length=1, choices=gender_choices, blank=False)
    # Things like specialties, background, qualifications and other info can be specified here.
    professional_info = models.JSONField(default=dict)

    def save(self, *args, **kwargs):
        if not self.user.is_doctor:
            raise ValidationError("User must be doctor to have a doctors profile")

        super().save(*args, **kwargs)

