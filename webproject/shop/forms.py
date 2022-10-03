from django import forms
from django.forms import widgets


class SearchForm(forms.Form):
    title = forms.CharField(
        max_length=100,
        required = True,
        widget=widgets.TextInput(attrs={'class': 'form-control', 'type': 'search', 'placeholder': 'поиск'})
    )