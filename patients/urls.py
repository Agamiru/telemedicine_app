from django.urls import path

from .views import RegisterPatient


urlpatterns = [
    path("", RegisterPatient.as_view())
]