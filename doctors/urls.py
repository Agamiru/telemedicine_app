from django.urls import path

from .views import RegisterDoctor


urlpatterns = [
    path("", RegisterDoctor.as_view())
]