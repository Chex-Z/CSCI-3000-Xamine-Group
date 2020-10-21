from django.urls import path

from . import views

urlpatterns = [
path("", views.patient_home_view, name="patient_home_view"),
path("patient_insurance", views.patient_insurance_view, name="patient_insurance_view"),
path("patient_account", views.patient_account_view, name="patient_account_view"),
path("patient_visits", views.patient_visits_view, name="patient_visits_view"),
path("patient_billing", views.patient_billing_view, name="patient_billing_view"),
path("patient_login", views.patient_login_view, name="patient_login"),
]