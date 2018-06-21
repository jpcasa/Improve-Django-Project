from django import forms
from django.forms.widgets import SelectDateWidget

from .models import Menu, Item, Ingredient

class MenuForm(forms.ModelForm):
    expiration_date=forms.DateField(
        widget=forms.TextInput(
            attrs= {'class':'datepicker'}
        )
    )

    class Meta:
        model = Menu
        exclude = ('created_date',)
