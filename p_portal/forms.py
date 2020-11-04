from django import forms
from django.contrib.auth import login, authenticate
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User

from xamine.models import Patient
from django.core.exceptions import ValidationError

# check emails in xamine.models.Patient
def is_patient(email):
    return Patient.objects.filter(email_info=email).exists()

#Registration form
class RegisterForm(UserCreationForm):
    email = forms.EmailField()

    class Meta:
        model = User
        fields = ["username", "email", "password1", "password2"]

    
    # used in .is_valid in p_portal.views
    def clean_email(self):
        data = self.cleaned_data.get('email')

        if not is_patient(data):
            raise forms.ValidationError('This email is not recognized by our system')

        return data


class PatientModelForm(forms.ModelForm):
    class Meta:
        model = Patient
        fields =[
            'phone_number',
            'first_name',
            'middle_name',
            'last_name',
            'phone_number',
            'insurance',
            'street',
            'city',
            'state',
            'zip_code',
        ]