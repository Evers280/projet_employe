from django import forms
from .models import *





class EmployeForm(forms.ModelForm):
    class Meta:
        model = Employe
        fields = ['nom', 'prenom', 'email', 'poste', 'salaire']
        
        widgets = {
            'nom': forms.TextInput(attrs={'class': 'input input-primary w-full', 'placeholder': 'Nom'}),
            'prenom': forms.TextInput(attrs={'class': 'input input-primary w-full', 'placeholder': 'Prénom'}),
            'email': forms.EmailInput(attrs={'class': 'input input-primary w-full', 'placeholder': 'Email'}),
            'poste': forms.TextInput(attrs={'class': 'input input-primary w-full', 'placeholder': 'Poste'}),
            'salaire': forms.NumberInput(attrs={'class': 'input input-primary w-full', 'placeholder': 'Salaire', 'min': '0','step': '0.01'}),
        }
 
    def clean_email(self):
        email = self.cleaned_data.get('email')
        # Vérifie si un *autre* employé avec cet email existe déjà.
        # On exclut l'instance actuelle (self.instance) de la requête.
        if Employe.objects.filter(email=email).exclude(pk=self.instance.pk).exists():
            raise forms.ValidationError("Un autre employé utilise déjà cette adresse email.")
        return email