from django.shortcuts import render, redirect
from django.contrib.auth.models import Group
from django.http import HttpResponseRedirect

from xamine.models import Patient

from .forms import RegisterForm


# Create your views here.
def patient_home_view(request):
    print ('print statement: ', request.user.first_name)
    p_user=Patient.objects.get(patient_user=request.user)
    print ('print first and last name', p_user.first_name, p_user.last_name)
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

        # extra validation to check email across xamine.models.Patient
        if form.is_valid():
            user = form.save()
            user_group = Group.objects.get(name='Patient')     
            user.groups.add(user_group)

            # find associated email in xamine.models.Patient and add user to Patient model
            xamine_patient = Patient.objects.get(email_info=response.POST.get('email'))
            xamine_patient.patient_user = user
            xamine_patient.save(update_fields=['patient_user'])

            # TODO remove
            # get the patient user name from xamine Patient model
            user.first_name = xamine_patient.first_name
            user.last_name = xamine_patient.last_name
            user.save(update_fields=['first_name', 'last_name'])

            return HttpResponseRedirect("/login/?next=/")
    else:
        form = RegisterForm()    

    return render(response, "register/register.html", {'form':form})

