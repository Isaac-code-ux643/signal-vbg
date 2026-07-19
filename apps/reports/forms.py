from django import forms
from .models import Report


class ReportForm(forms.ModelForm):
    class Meta:
        model = Report
        fields = [
            'vbg_type', 'title', 'description', 'date_of_incident',
            'location_description', 'latitude', 'longitude', 'urgency',
            'is_anonymous', 'contact_name', 'contact_phone', 'contact_email'
        ]
        widgets = {
            'title': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Décrivez brièvement la situation'
            }),
            'description': forms.Textarea(attrs={
                'class': 'form-control', 'rows': 5,
                'placeholder': 'Donnez les détails que vous souhaitez partager...'
            }),
            'date_of_incident': forms.DateInput(attrs={
                'class': 'form-control', 'type': 'date'
            }),
            'location_description': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': "Lieu approximatif de l'incident"
            }),
            'latitude': forms.HiddenInput(),
            'longitude': forms.HiddenInput(),
            'urgency': forms.Select(attrs={'class': 'form-select'}),
            'vbg_type': forms.Select(attrs={'class': 'form-select'}),
            'is_anonymous': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
            'contact_name': forms.TextInput(attrs={
                'class': 'form-control', 'placeholder': 'Nom (optionnel)'
            }),
            'contact_phone': forms.TextInput(attrs={
                'class': 'form-control', 'placeholder': 'Téléphone (optionnel)'
            }),
            'contact_email': forms.EmailInput(attrs={
                'class': 'form-control', 'placeholder': 'Email (optionnel)'
            }),
        }


class ReportSearchForm(forms.Form):
    tracking_code = forms.CharField(
        max_length=12,
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'Entrez votre code de suivi (ex: VBG-XXXX-XXXX)'
        })
    )
