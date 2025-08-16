from django import forms
from .models import *
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm

class LoginForm(forms.Form):
    username = forms.CharField(max_length=150, widget=forms.TextInput(attrs={'class': 'input input-primary w-full', 'placeholder': "Nom d'utilisateur"}))
    password = forms.CharField(widget=forms.PasswordInput(attrs={'class': 'input input-primary w-full', 'placeholder': 'Mot de passe'}))

class DrhSignUpForm(UserCreationForm):
    
    class Meta(UserCreationForm.Meta):
        model = User
        fields = UserCreationForm.Meta.fields + ('email',)




class EmployeForm(forms.ModelForm):
    
    class Meta:
        model = Employe
        fields = ['nom', 'prenom', 'age', 'sexe', 'email', 'numero_telephone', 'poste', 'salaire', 'drh']
        
        widgets = {
            'nom': forms.TextInput(attrs={'class': 'input input-primary w-full', 'placeholder': 'Nom'}),
            'prenom': forms.TextInput(attrs={'class': 'input input-primary w-full', 'placeholder': 'Prénom'}),
            'age': forms.NumberInput(attrs={'class': 'input input-primary w-full', 'placeholder': 'Âge', 'min': '18'}),
            'sexe': forms.Select(attrs={'class': 'select select-primary w-full'}),
            'email': forms.EmailInput(attrs={'class': 'input input-primary w-full', 'placeholder': 'Email'}),
            'numero_telephone': forms.TextInput(attrs={'class': 'input input-primary w-full', 'placeholder': 'Numéro de téléphone'}),
            'poste': forms.TextInput(attrs={'class': 'input input-primary w-full', 'placeholder': 'Poste'}),
            'salaire': forms.NumberInput(attrs={'class': 'input input-primary w-full', 'placeholder': 'Salaire', 'min': '0','step': '0.01'}),
            'drh': forms.TextInput(attrs={'class': 'input input-primary w-full', 'placeholder': 'DRH'})
        }
 
    def clean_email(self):
        email = self.cleaned_data.get('email')
        # Vérifie si un *autre* employé avec cet email existe déjà.
        # On exclut l'instance actuelle (self.instance) de la requête.
        if Employe.objects.filter(email=email).exclude(pk=self.instance.pk).exists():
            raise forms.ValidationError("Un autre employé utilise déjà cette adresse email.")
        return email
    
    
    def __init__(self, *args, **kwargs):
        # Récupère 'drh' des arguments mot-clé avant d'appeler super().__init__
        drh = kwargs.pop('drh', False)
        super().__init__(*args, **kwargs)
        
        if drh:
            self.fields['password'] = forms.CharField(widget=forms.PasswordInput(attrs={'class': 'input input-primary w-full', 'placeholder': 'Mot de passe'}), required=True)
            self.fields['password_confirm'] = forms.CharField(widget=forms.PasswordInput(attrs={'class': 'input input-primary w-full', 'placeholder': 'Confirmer le mot de passe'}), required=True)
            if 'drh' in self.fields:
                del self.fields['drh']
            if 'poste' in self.fields:
                del self.fields['poste']
        else:
            if 'drh' in self.fields:
                del self.fields['drh']

    #méthode de validation personnalisée
    def clean(self):
        cleaned_data = super().clean()
        password = cleaned_data.get("password")
        password_confirm = cleaned_data.get("password_confirm")

        # Vérifie que les deux champs existent si le formulaire est pour un DRH
        if password and password_confirm:
            if password != password_confirm:
                # Lance une erreur si les mots de passe ne correspondent pas
                raise forms.ValidationError(
                    "Les deux mots de passe ne correspondent pas."
                )
        return cleaned_data

    def save(self, commit=True):
        employe = super().save(commit=False)
        
        if 'password' in self.cleaned_data:
            user = User.objects.create_user(
                username=self.cleaned_data['email'],
                email=self.cleaned_data['email'],
                password=self.cleaned_data['password']
            )
            employe.utilisateur = user

        if commit:
            employe.save()
        return employe



