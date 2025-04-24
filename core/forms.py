from django import forms
from .models import Client, Enrollment

class ClientForm(forms.ModelForm):
    class Meta:
        model = Client
        fields = ['full_name', 'age', 'contact']

class EnrollmentForm(forms.ModelForm):
    class Meta:
        model = Enrollment
        fields = ['client', 'program']
