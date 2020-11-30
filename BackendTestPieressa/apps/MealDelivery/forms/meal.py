from django import forms
from django.forms import formset_factory

class MealForm(forms.Form):
    """A class form used to create new meals for a menu of a certain date."""
    name = forms.CharField(
        label='Meal Name',
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'Enter Meal Name here'
        })
    )

MealFormset = formset_factory(MealForm, extra=1)
