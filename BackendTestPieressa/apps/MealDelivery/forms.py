from django import forms
from django.forms import formset_factory
from .models import Employee
from datetime import date

class MealForm(forms.Form):
    name = forms.CharField(
        label='Meal Name',
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'Enter Meal Name here'
        })
    )

MealFormset = formset_factory(MealForm, extra=1)

class EmployeeForm(forms.ModelForm):
    class Meta:
        model = Employee
        fields = ['username', 'name']

class DateForm(forms.Form):
    date = forms.DateField(
        label='Date',
        widget=forms.DateInput(attrs={
            'class': 'form-control',
            'placeholder': 'Enter Meal Name here'
        })
    )

class SelectedMenuForm(forms.Form):

    def __init__(self, choices):
        super().__init__()
        self.fields['meal'] = forms.ChoiceField(
            label='Meal',
            choices=choices
        )
        self.fields['customization'] = forms.CharField(
            label='Customizations',
            widget=forms.Textarea(attrs={
                'class': 'form-control',
                'placeholder': 'Enter any meal customizations (optional)'
            })
        )
