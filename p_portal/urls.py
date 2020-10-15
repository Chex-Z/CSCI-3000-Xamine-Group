from django.urls import path

from . import views

urlpatterns = [
path("", views.patient_home_view, name="patient_home_view"),
path("patient_insurance", views.patient_insurance_view, name="patient_insurance_view"),
path("patient_account", views.patient_account_view, name="patient_account_view"),
]