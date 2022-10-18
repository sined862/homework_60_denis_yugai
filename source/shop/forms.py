from django import forms
from django.forms import ValidationError
from shop.models import CategoryChoices, Product, Order 


def balance_length_validator(number):
    if (number) < 0:
        raise ValidationError("Остаток на складне не должен быть меньше нуля!")
    return number

class ProductForm(forms.ModelForm):
    balance = forms.IntegerField(
        validators=(balance_length_validator,),
        label='Баланс',
        widget=forms.TextInput(attrs={'class': 'form-control'})
    )

    class Meta:
        model = Product
        fields = ('title', 'description', 'photo', 'category', 'balance', 'price')
        widgets = {
            'title' : forms.TextInput(attrs={'class': 'form-control'}),
            'description': forms.Textarea(attrs={'class': 'form-control', 'style': 'height:150px'}),
            'category': forms.RadioSelect,
            'photo' : forms.TextInput(attrs={'class': 'form-control'}),
            'price' : forms.TextInput(attrs={'class': 'form-control'})
        }



class SearchForm(forms.Form):
    search = forms.CharField(max_length=100, required=False, label='Найти')


class OrderForm(forms.ModelForm):
    class Meta:
        model = Order
        fields = ('name', 'phone', 'address')