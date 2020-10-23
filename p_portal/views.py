from django.shortcuts import render, redirect
from .forms import RegisterForm
from django.contrib.auth.models import Group

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

def patient_login_view(request):
    return render(request, "patient_login.html", {})

#Register User as Patient
def register(response):
    if response.method == "POST":
        form = RegisterForm(response.POST)
        if form.is_valid():
            user = form.save()
            user_group = Group.objects.get(name='Patient')         
            user.groups.add(user_group)
            
            return redirect("/login")
    else:
        form = RegisterForm()    

    return render(response, "register/register.html", {'form':form})    

