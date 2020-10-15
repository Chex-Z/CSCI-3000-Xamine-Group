from django.shortcuts import render

# Create your views here.
def patient_home_view(request):
    return render(request, "patient_home_template.html", {})