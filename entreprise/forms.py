from django import forms
from .models import *


class EntrepriseForm(forms.ModelForm):
    
    class Meta:
        model = entreprises
        fields = ['nom_entreprise', 'adresse_siege', 'code_postal', 'ville', 'pays', 'telephone_entreprise', 'email', 'numero_siret', 'code_naf', 'forme_juridique', 'secteur_activite', 'nombre_employes']
        
        widgets = {
            'nom_entreprise': forms.TextInput(attrs={'class': 'input input-primary w-full', 'placeholder': 'Nom de l\'entreprise'}),
            'adresse_siege': forms.TextInput(attrs={'class': 'input input-primary w-full', 'placeholder': 'Adresse'}),
            'code_postal': forms.TextInput(attrs={'class': 'input input-primary w-full', 'placeholder': 'Code postal'}),
            'ville': forms.TextInput(attrs={'class': 'input input-primary w-full', 'placeholder': 'Ville'}),
            'pays': forms.TextInput(attrs={'class': 'input input-primary w-full', 'placeholder': 'Pays'}),
            'telephone_entreprise': forms.TextInput(attrs={'class': 'input input-primary w-full', 'placeholder': 'Téléphone'}),
            'email': forms.EmailInput(attrs={'class': 'input input-primary w-full', 'placeholder': 'Email'}),
            'numero_siret': forms.TextInput(attrs={'class': 'input input-primary w-full', 'placeholder': 'Numéro SIRET'}),
            'code_naf': forms.TextInput(attrs={'class': 'input input-primary w-full', 'placeholder': 'Code NAF'}),
            'forme_juridique': forms.Select(attrs={'class': 'select select-primary w-full '}),
            'secteur_activite': forms.Select(attrs={'class': 'select select-primary w-full'}),
            'nombre_employes': forms.NumberInput(attrs={'class': 'input input-primary w-full', 'placeholder': 'Nombre d\'employés', 'min': '1'})
        }
        
        
        
class ServiceForm(forms.ModelForm):
  
    class Meta:
        model = services
        fields = ['nom_service', 'numero_service', 'email_service', 'budget_annuel', 'objectifs_service']
        
        widgets = {
            'nom_service': forms.TextInput(attrs={'class': 'input input-primary w-full', 'placeholder': 'Nom du service'}),
            'numero_service': forms.TextInput(attrs={'class': 'input input-primary w-full', 'placeholder': 'Numéro du service'}),
            'email_service': forms.EmailInput(attrs={'class': 'input input-primary w-full', 'placeholder': 'Email du service'}),
            'budget_annuel': forms.NumberInput(attrs={'class': 'input input-primary w-full', 'placeholder': 'Budget annuel'}),
            'objectifs_service': forms.Textarea(attrs={'class': 'textarea textarea-primary w-full', 'placeholder': 'Objectifs du service'})
        }        