from django.core.exceptions import ValidationError
from django.forms.models import  BaseModelForm, ModelFormMetaclass
from .models import Unavailable, Appointment

from django.utils import timezone


# An abstract form that inherits methods used by both Appointment and UnavailableTime
# models to perform cleaning that are unique to them both.
class AbstractDurationForm(BaseModelForm, metaclass=ModelFormMetaclass):

    def clean(self):
        self.extra_checks()
        super().clean()

    def extra_checks(self, model=None):
        # Field sanity checks
        self.check_future_time("start_time")
        self.check_future_time("end_time")
        self.check_positive_duration("start_time", "end_time")
        # Overlaps
        if not model:
            model = self._meta.model
        self.check_for_overlaps(model)

    def check_for_overlaps(self, model):
        message = "Please set an earlier or later date"
        doctor = self.cleaned_data.get("doctor")
        start_time = self.cleaned_data.get("start_time")
        end_time = self.cleaned_data.get("end_time")
        model = model
        doctors_appointments = model.objects.filter(doctor=doctor)
        # Check for overlapping appointments
        if doctors_appointments.filter(start_time=start_time):
            raise ValidationError({"start_time": message})
        if doctors_appointments.filter(start_time__lt=start_time) \
                .filter(end_time__gte=start_time):
            raise ValidationError({"start_time": message})
        if doctors_appointments.filter(start_time__gt=start_time) \
                .filter(start_time__lt=end_time):
            raise ValidationError({"start_time": message})

    # Check that time filled in form isn't in the past or present
    def check_future_time(self, field: str):
        now = timezone.now()
        time_to_set = self.cleaned_data.get(field)
        time_delta = time_to_set - now
        if time_delta.total_seconds() <= 0:
            raise ValidationError({field: "Please set a later time"})

    # Check that ending is ahead of starting
    def check_positive_duration(self, field_1: str, field_2: str):
        earlier = self.cleaned_data.get(field_1)
        later = self.cleaned_data.get(field_2)
        time_delta = later - earlier

        if time_delta.total_seconds() <= 0:
            message = f"{field_2.title()} time must be ahead of {field_1.title()} time."
            raise ValidationError({field_2: message})


class UnavailableForm(AbstractDurationForm):

    class Meta:
        model = Unavailable
        exclude = ["duration", "created"]


class AppointmentForm(AbstractDurationForm):
    def extra_checks(self, model=None):
        super().extra_checks()
        model = Unavailable
        self.check_for_overlaps(model)

    class Meta:
        model = Appointment
        exclude = ["duration, created"]