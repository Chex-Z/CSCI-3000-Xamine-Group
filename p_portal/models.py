from django.contrib.auth.models import User
from django.db import models

class Insurance(models.Model):
    insurance_user = models.ForeignKey(User, related_name='insurance_user', on_delete=models.SET_NULL, null=True, blank=True)
    company_name = models.CharField(max_length=128)
    account_holder = models.CharField(max_length=128)
    group_number = models.CharField(max_length=32)
    account_number = models.CharField(max_length=32)
    contact_number = models.CharField(max_length=32)
    coverage = models.FloatField(default=0.0)

    def __str__(self):
        return f"{self.company_name} ({self.id})"