from django.urls import path

from . import views

urlpatterns = [
path("", views.patient_home_view, name="patient_home_view"),
]