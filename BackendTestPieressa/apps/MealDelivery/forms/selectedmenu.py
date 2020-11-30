from django import forms

class SelectedMenuForm(forms.Form):
    """
    Form used by employees to select a meal from the daily menus.

    Attributes
    ----------
    choices ((string, string)[]): List of tuples containing meal's id and name

    Methods
    -------
    __init__(choices)
        Edits the Class initialization to contain possible meal choices
    """

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
