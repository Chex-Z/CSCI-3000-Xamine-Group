from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.http import Http404
from django.contrib.auth import update_session_auth_hash
from django.contrib.auth.forms import PasswordChangeForm
from django.contrib.auth.models import Group
from django.http import HttpResponseRedirect
from django.views.generic import DetailView, UpdateView
from django.core.mail import send_mail
from django.views.generic import DetailView, UpdateView, CreateView

from xamine.models import Patient, Order, Payment, Invoice
from .models import Insurance
from .forms import RegisterForm, PatientModelForm, PaymentForm, InsuranceModelForm


# Create your views here.
def patient_home_view(request):
    """ get patient user and patient user oder set """
    p_user=Patient.objects.get(patient_user=request.user)
    p_orders=Order.objects.filter(patient=p_user)

    # Set up empty context to pass to template
    context = {}

    """ upcoming appointments """
    upcoming_orders = Order.objects.filter(level_id=1, appointment__isnull=False).order_by('appointment')

    """ orders """
    complete_orders = p_orders.filter(level_id=4).order_by('completed_time')
    active_orders = p_orders.filter(level_id__lt=4)

    # context['active_orders'] = active_orders
    context['complete_orders'] = complete_orders
    context['upcoming_orders'] = upcoming_orders

    return render(request, "patient_home_template.html", context)
    
# Display patient info on Account tab
class PatientDetailView(DetailView):
    template_name = 'patient_detail.html'
    queryset = Patient.objects.all()

    def get_object(self):
        id_ = Patient.objects.get(patient_user=self.request.user).id
        return get_object_or_404(Patient, id=id_)

# Change account info in account tab
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

# insurance detail information
def insurance_view(request):
    # provides context for what to show on insurance_detail.html
    insurance_exists = Insurance.objects.filter(insurance_user=request.user).exists()

    context = { 'insurance_exists': insurance_exists}

    # if the user does no thave any insurance then there is no instance to grab
    if insurance_exists:
        patient_insurance = Insurance.objects.get(insurance_user=request.user)
        context['object'] = patient_insurance

    return render(request, "insurance_detail.html",context)

# Create an insurance instance for the user if none exists
class InsuranceCreateView(CreateView):
    template_name = 'insurance_create.html'
    form_class = InsuranceModelForm
    queryset = Insurance.objects.all()
    success_url = '/patient_portal/insurance'

    # in addition to creating the insurance instance the user is added to foreign key
    def form_valid(self, form):
        print(form.cleaned_data)
        this_instance = form.save()

        this_instance.insurance_user = self.request.user

        this_instance.save(update_fields=['insurance_user'])
        return super().form_valid(form)

# Change insurance info in insurance tab
class InsuranceUpdateView(UpdateView):
    template_name = 'insurance_update.html'
    form_class = InsuranceModelForm
    success_url = '/patient_portal/insurance'

    def get_object(self):
        id_ = Insurance.objects.get(insurance_user=self.request.user).id
        return get_object_or_404(Insurance, id=id_)

    def form_valid(self, form):
        print(form.cleaned_data)
        return super().form_valid(form)

def patient_visits_view(request):
    return render(request, "visits_template.html", {})

#for patient visits
#grabs appointment info
def appointment(request):
    if request.method == "POST":
        your_name = request.POST['your-name']
        your_phone = request.POST['your-phone']
        your_email = request.POST['your-email']
        your_address = request.POST['your-address']
        your_date = request.POST['your-date']
        your_schedule = request.POST['your-schedule']
        your_message = request.POST['your-message']

    
        #send email to receptionist 
        appointment = "Name: " + your_name + " Phone: " + your_phone + " Email: " + your_email + " Address: " + your_address + " Requested Date: " + your_date + " Requested Time: " + your_schedule + " Message: " + your_message
        
        send_mail(
            'Appointment Request', # subject
            appointment, # message
            your_email, #from email
            ['ris.system.scheduling@gmail.com'] # email being sent to
        )
        #return values
        return render(request, 'appointment.html', {
            'your_name': your_name,
            'your_phone': your_phone,
            'your_email': your_email,
            'your_address': your_address,
            'your_date': your_date,
            'your_schedule': your_schedule,
            'your_message': your_message
        })
    
    else:
        return render(request, 'visits_template.html', {})

def patient_billing_view(request):
    """ get patient user and patient user oder set """
    p_user=Patient.objects.get(patient_user=request.user)
    p_invoice=Invoice.objects.filter(patient=p_user)
    # Set up empty context to pass to template
    context = {}

    current_invoices = p_invoice.filter(isPaid=False).order_by('order_id')
    context['invoices'] = current_invoices
    return render(request, "billing_template.html", context)

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

def add_card(request):
    print("current user:" , request.user)
    if request.method == 'POST':
        form = PaymentForm(request.POST, instance = Payment(patient_user = request.user))
        if form.is_valid():
            form.save()
            return redirect('/patient_portal/patient_billing')
    else:
        form = PaymentForm()  
    return render(request, 'add_card.html', {'form':form})

def cancel_order(request, order_id):
    try:
        cur_order = Order.objects.get(pk=order_id)
    except Order.DoesNotExist:
        raise Http404

    context = {
        'this_order': cur_order
    }
    
    if request.method == 'POST':
	    cur_order.delete()
	    return redirect('/..')
    return render(request, 'cancel_order.html', context)

def remove_insurance(request):
    cur_insurance = Insurance.objects.get(insurance_user=request.user)

    context = {
        'this_insurance': cur_insurance
    }
    
    if request.method == 'POST':
	    cur_insurance.delete()
	    return redirect('/patient_portal/insurance')
    return render(request, 'remove_insurance.html', context)