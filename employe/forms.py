from django import forms
from .models import *
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from .posts import POSTES_PAR_SECTEUR
from entreprise.models import services as ServicesEntreprise

class LoginForm(forms.Form):
    username = forms.CharField(max_length=150, widget=forms.TextInput(attrs={'class': 'input input-primary w-full', 'placeholder': "Nom d'utilisateur"}))
    password = forms.CharField(widget=forms.PasswordInput(attrs={'class': 'input input-primary w-full', 'placeholder': 'Mot de passe'}))

class DrhSignUpForm(UserCreationForm):
    
    class Meta(UserCreationForm.Meta):
        model = User
        fields = UserCreationForm.Meta.fields + ('email',)

class EmployeForm(forms.ModelForm):
    poste = forms.ChoiceField(
        required=True,
        widget=forms.Select(attrs={'class': 'select select-primary w-full'}),
        label="Poste"
    )
    poste_autre = forms.CharField(required=False, label="Autre poste", widget=forms.TextInput(attrs={'class': 'input input-primary w-full', 'placeholder': 'Précisez le poste'}))

    class Meta:
        model = Employe
        fields = ['nom', 'prenom', 'age', 'sexe', 'email', 'numero_telephone', 'service', 'poste', 'salaire', 'drh']
        widgets = {
            'nom': forms.TextInput(attrs={'class': 'input input-primary w-full', 'placeholder': 'Nom'}),
            'prenom': forms.TextInput(attrs={'class': 'input input-primary w-full', 'placeholder': 'Prénom'}),
            'age': forms.NumberInput(attrs={'class': 'input input-primary w-full', 'placeholder': 'Âge', 'min': '18'}),
            'sexe': forms.Select(attrs={'class': 'select select-primary w-full'}),
            'email': forms.EmailInput(attrs={'class': 'input input-primary w-full', 'placeholder': 'Email'}),
            'numero_telephone': forms.TextInput(attrs={'class': 'input input-primary w-full', 'placeholder': 'Numéro de téléphone'}),
            'service': forms.Select(attrs={'class': 'select select-primary w-full'}),
            'salaire': forms.NumberInput(attrs={'class': 'input input-primary w-full', 'placeholder': 'Salaire', 'min': '0','step': '0.01'}),
            'drh': forms.TextInput(attrs={'class': 'input input-primary w-full', 'placeholder': 'DRH'})
        }
 
    def __init__(self, *args, **kwargs):
        drh = kwargs.pop('drh', False)
        entreprise = kwargs.pop('entreprise', None)
        super().__init__(*args, **kwargs)

        if entreprise:
            self.fields['service'].queryset = ServicesEntreprise.objects.filter(entreprise=entreprise).all()

            secteur = entreprise.secteur_activite
            poste_choices = []
            
            secteur_services = POSTES_PAR_SECTEUR.get(secteur, {})
            for service_name, postes in secteur_services.items():
                poste_choices.append((service_name, [(poste, poste) for poste in postes]))

            communs_services = POSTES_PAR_SECTEUR.get('Communs', {})
            for service_name, postes in communs_services.items():
                poste_choices.append((service_name, [(poste, poste) for poste in postes]))

            self.fields['poste'].choices = [('', '---------')] + poste_choices + [('Autre', 'Autre')]
        else:
            self.fields['poste'].choices = [('Autre', 'Autre')]

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

    def clean_email(self):
        email = self.cleaned_data.get('email')
        if Employe.objects.filter(email=email).exclude(pk=self.instance.pk).exists():
            raise forms.ValidationError("Un autre employé utilise déjà cette adresse email.")
        return email
    
    def clean(self):
        cleaned_data = super().clean()
        poste = cleaned_data.get('poste')
        poste_autre = cleaned_data.get('poste_autre')

        if poste == 'Autre':
            if not poste_autre:
                self.add_error('poste_autre', "Veuillez préciser le poste.")
            else:
                cleaned_data['poste'] = poste_autre
        
        password = cleaned_data.get("password")
        password_confirm = cleaned_data.get("password_confirm")

        if password and password_confirm:
            if password != password_confirm:
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
