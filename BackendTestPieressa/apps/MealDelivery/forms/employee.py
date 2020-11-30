from django import forms
from ..models.employee import Employee

class EmployeeForm(forms.ModelForm):
    """A class Metaform used to create new employees for the system.
    The username provided must be their slack Id to receive meal reminders."""
    class Meta:
        """Employee's ModelForm metadata, that represents the model used and
        the fields to fill from model"""
        model = Employee
        fields = ['username', 'name']
