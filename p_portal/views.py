from django.shortcuts import render

# Create your views here.
def patient_home_view(request):
    return render(request, "patient_home_template.html", {})

def patient_account_view(request):
    return render(request, "account_template.html", {})

def patient_insurance_view(request):
    return render(request, "insurance_template.html", {})

def patient_visits_view(request):
    return render(request, "visits_template.html", {})

def patient_billing_view(request):
    return render(request, "billing_template.html", {})

