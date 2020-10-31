from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.contrib.auth import update_session_auth_hash
from django.contrib.auth.forms import PasswordChangeForm
from django.contrib.auth.models import Group
from django.http import HttpResponseRedirect
from django.views.generic import DetailView, UpdateView

from xamine.models import Patient

from .forms import RegisterForm, PatientModelForm


# Create your views here.
def patient_home_view(request):
    # p_user=Patient.objects.get(patient_user=request.user)
    # print ('print statement: ', Patient.objects.get(patient_user=request.user).id)
    return render(request, "patient_home_template.html", {})
    
class PatientDetailView(DetailView):
    template_name = 'patient_detail.html'
    queryset = Patient.objects.all()

    def get_object(self):
        id_ = Patient.objects.get(patient_user=self.request.user).id
        return get_object_or_404(Patient, id=id_)

class PatientUpdateView(UpdateView):
    template_name = 'patient_update.html'
    form_class = PatientModelForm
    success_url = '/patient_portal/detail'

    def get_object(self):
        id_ = Patient.objects.get(patient_user=self.request.user).id
        return get_object_or_404(Patient, id=id_)

    def form_valid(self, form):
        print(form.cleaned_data)
        return super().form_valid(form)

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

def change_password(request):
    if request.method == 'POST':
        form = PasswordChangeForm(request.user, request.POST)
        if form.is_valid():
            user = form.save()
            update_session_auth_hash(request, user)  # Important!
            messages.success(request, 'Your password was successfully updated!')
            return redirect('change_password')
        else:
            messages.error(request, 'Please correct the error below.')
    else:
        form = PasswordChangeForm(request.user)
    return render(request, 'change_password.html', {
        'form': form
    })