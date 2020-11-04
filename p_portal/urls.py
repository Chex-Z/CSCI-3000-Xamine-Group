from django.urls import path, include
from django.conf.urls import url

from . import views


urlpatterns = [
path("", views.patient_home_view, name="patient_home_view"),
url(r'^password/$', views.change_password, name='change_password'),
path("patient_insurance", views.patient_insurance_view, name="patient_insurance_view"),
path("detail", views.PatientDetailView.as_view(), name="patient_account_view"),
path("detail/update", views.PatientUpdateView.as_view(), name="patient_update_view"),
path("patient_visits", views.patient_visits_view, name="patient_visits_view"),
path("patient_billing", views.patient_billing_view, name="patient_billing_view"),

#Register
path("register", views.register, name="register"),
]