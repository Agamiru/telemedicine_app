from django.urls import path

from .views import CreateAppointment, CreateUnavailable


urlpatterns = [
    path("<int:user_id>/", CreateAppointment.as_view()),
    path("unavailable/<int:user_id>/", CreateUnavailable.as_view())
]