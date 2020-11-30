from django import forms

class DateForm(forms.Form):
    """A class form used to add a date parameter."""
    date = forms.DateField(
        label='Date',
        widget=forms.DateInput(attrs={
            'class': 'form-control',
            'placeholder': 'Enter Meal Name here'
        })
    )
