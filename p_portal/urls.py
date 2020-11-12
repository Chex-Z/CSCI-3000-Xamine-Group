from django.urls import path, include
from django.conf.urls import url

from . import views


urlpatterns = [
path("", views.patient_home_view, name="patient_home_view"),
url(r'^password/$', views.change_password, name='change_password'),
path("add_card", views.add_card, name="add_card"),
path("insurance", views.insurance_view, name="patient_insurance_view"),
path("insurance/add", views.InsuranceCreateView.as_view(), name="insurance_create_view"),
path("insurance/update", views.InsuranceUpdateView.as_view(), name="insurance_update_view"),
path('insurance/remove', views.remove_insurance, name='remove_insurance'),
path("detail", views.PatientDetailView.as_view(), name="patient_account_view"),
path("detail/update", views.PatientUpdateView.as_view(), name="patient_update_view"),
path("patient_visits", views.patient_visits_view, name="patient_visits_view"),
path("patient_billing", views.patient_billing_view, name="patient_billing_view"),
path('cancel_order/<int:order_id>/', views.cancel_order, name='cancel_order'),

#Register
path("register", views.register, name="register"),
]