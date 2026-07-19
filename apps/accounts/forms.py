from django import forms
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from .models import User


class VictimRegistrationForm(UserCreationForm):
    email = forms.EmailField(required=False, widget=forms.EmailInput(
        attrs={'class': 'form-control', 'placeholder': 'Email (optionnel)'}
    ))
    phone = forms.CharField(max_length=20, required=False, widget=forms.TextInput(
        attrs={'class': 'form-control', 'placeholder': 'Téléphone (optionnel)'}
    ))

    class Meta:
        model = User
        fields = ['username', 'password1', 'password2', 'email', 'phone']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['username'].widget.attrs.update({
            'class': 'form-control',
            'placeholder': "Nom d'utilisateur"
        })
        self.fields['password1'].widget.attrs.update({
            'class': 'form-control',
            'placeholder': 'Mot de passe'
        })
        self.fields['password2'].widget.attrs.update({
            'class': 'form-control',
            'placeholder': 'Confirmer le mot de passe'
        })


class CustomLoginForm(AuthenticationForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['username'].widget.attrs.update({
            'class': 'form-control',
            'placeholder': "Nom d'utilisateur"
        })
        self.fields['password'].widget.attrs.update({
            'class': 'form-control',
            'placeholder': 'Mot de passe'
        })
