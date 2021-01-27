import datetime
from typing import Optional

from django.utils import timezone
from django.db import models
from django.core.exceptions import ValidationError

from doctors.models import Doctor
from patients.models import Patient

# Create your models here.


# Appointments and Unavailable inherit from this
class AbstractAppointmentModel(models.Model):
    start_time = models.DateTimeField()
    end_time = models.DateTimeField()
    # Duration is in hours/mins in format '2.30'
    # This field is mainly for indexing as it can be easily computed using
    # start_time and end_time values.
    duration = models.FloatField(blank=True)
    created = models.DateTimeField(default=timezone.now, blank=True)

    def _time_delta_in_seconds(self) -> int:
        time_delta = (self.end_time - self.start_time)
        return time_delta.total_seconds()

    # Set and format duration before saving
    def save(self, *args, **kwargs):
        in_hours = self._time_delta_in_seconds() / 3600
        format_dur = float("{:.2f}".format(in_hours))
        self.duration = format_dur
        super().save(*args, **kwargs)

    class Meta:
        abstract = True


class Appointment(AbstractAppointmentModel):
    # Set Null on delete, so another doctor can be assigned to the patient
    # at a later time without creating a new appointment.
    doctor = models.ForeignKey(
        Doctor, on_delete=models.SET_NULL, related_name="appointment",
        null=True
    )
    # Cascade on delete, no need keeping appointment.
    patient = models.ForeignKey(
        Patient, on_delete=models.CASCADE, related_name="appointment"
    )


class Unavailable(AbstractAppointmentModel):
    doctor = models.ForeignKey(
        Doctor, on_delete=models.CASCADE, related_name="unavailable",
    )

    def duration_in_mins(self) -> int:
        in_secs = self._time_delta_in_seconds()
        if in_secs >= 60:
            return in_secs // 60

    def duration_in_hours(self) -> Optional[int]:
        in_mins = self.duration_in_mins()
        if in_mins >= 60:
            return in_mins // 60

    def get_pretty_duration(self):
        if self.duration_in_hours() is None:
            return f"{self.duration_in_mins()} mins"
        else:
            in_hours = self.duration_in_hours()
            if in_hours < 24:
                return f"{in_hours} hours"
            else:
                result = in_hours // 24
                if result > 0:
                    if result < 7:
                        return f"{result} days"
                    elif 7 <= result < 30:
                        return f"{result} weeks"
                    elif 30 <= result < 365:
                        return f"{result} months"
                    else:
                        raise ValueError(f"Duration of {in_hours} hours too long for an appointment")

    def __str__(self):
        formatted_start_date = self.start_time.strftime("%d/%m/%Y - %I:%M:%S %p")
        return f"unavailable for {self.get_pretty_duration()} starting from {formatted_start_date}"