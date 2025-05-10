from django import forms
from .models import UtenteRegistrato
from django.core.exceptions import ValidationError

class RegistrazioneForm(forms.ModelForm):
    class Meta:
        model = UtenteRegistrato
        fields = ['nome', 'email']
        labels = {
            'nome': 'Nome',
            'email': 'Email',
        }
        """widgets = {
            'nome': forms.TextInput(attrs={'placeholder': 'Es: Zio Pippo'}),
            'email': forms.EmailInput(attrs={'placeholder': 'esempio@mail.com'}),
        }"""

    def clean_email(self):
        email = self.cleaned_data['email']
        if UtenteRegistrato.objects.filter(email=email).exists():
            raise ValidationError("Questa email è già registrata")
        return email