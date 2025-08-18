from django import forms
from .models import *
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from .posts import POSTES_PAR_SECTEUR
from entreprise.models import services as ServicesEntreprise

# Formulaire de connexion utilisateur
class LoginForm(forms.Form):
    username = forms.CharField(
        max_length=150,
        widget=forms.TextInput(attrs={'class': 'input input-primary w-full', 'placeholder': "Nom d'utilisateur"}),
        label="Nom d'utilisateur" # Ajout d'un label explicite
    )
    password = forms.CharField(
        widget=forms.PasswordInput(attrs={'class': 'input input-primary w-full', 'placeholder': 'Mot de passe'}),
        label="Mot de passe" # Ajout d'un label explicite
    )

# Formulaire d'inscription pour les utilisateurs DRH (hérite de UserCreationForm de Django)
class DrhSignUpForm(UserCreationForm):
    class Meta(UserCreationForm.Meta):
        model = User
        # Ajoute le champ 'email' aux champs par défaut du formulaire de création d'utilisateur
        fields = UserCreationForm.Meta.fields + ('email',)

# Formulaire pour la création et la modification d'un employé
class EmployeForm(forms.ModelForm):
    # Champ personnalisé pour le poste de l'employé, avec des choix dynamiques
    poste = forms.ChoiceField(
        required=True,
        widget=forms.Select(attrs={'class': 'select select-primary w-full'}),
        label="Poste"
    )
    # Champ optionnel pour spécifier un poste si "Autre" est sélectionné
    poste_autre = forms.CharField(
        required=False,
        label="Autre poste",
        widget=forms.TextInput(attrs={'class': 'input input-primary w-full', 'placeholder': 'Précisez le poste'})
    )

    class Meta:
        model = Employe # Modèle associé à ce formulaire
        # Champs du modèle Employe à inclure dans le formulaire
        fields = ['nom', 'prenom', 'age', 'sexe', 'email', 'numero_telephone', 'service', 'poste', 'salaire', 'drh']
        # Widgets personnalisés pour les champs du formulaire afin d'appliquer des styles CSS
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
 
    # Méthode d'initialisation du formulaire, appelée lors de sa création
    def __init__(self, *args, **kwargs):
        # Récupère les arguments spécifiques 'drh' et 'entreprise' et les retire des kwargs
        drh = kwargs.pop('drh', False)
        entreprise = kwargs.pop('entreprise', None)
        super().__init__(*args, **kwargs) # Appelle l'initialisation de la classe parente

        # Si une entreprise est fournie, filtre les services disponibles pour l'employé
        if entreprise:
            self.fields['service'].queryset = ServicesEntreprise.objects.filter(entreprise=entreprise).all()

            # Génère les choix de postes basés sur le secteur d'activité de l'entreprise
            secteur = entreprise.secteur_activite
            poste_choices = []
            
            # Ajoute les postes spécifiques au secteur de l'entreprise
            secteur_services = POSTES_PAR_SECTEUR.get(secteur, {})
            for service_name, postes in secteur_services.items():
                poste_choices.append((service_name, [(poste, poste) for poste in postes]))

            # Ajoute les postes communs à tous les secteurs
            communs_services = POSTES_PAR_SECTEUR.get('Communs', {})
            for service_name, postes in communs_services.items():
                poste_choices.append((service_name, [(poste, poste) for poste in postes]))

            # Définit les choix du champ 'poste', incluant une option "Autre"
            self.fields['poste'].choices = [('', '---------')] + poste_choices + [('Autre', 'Autre')]
        else:
            # Si aucune entreprise n'est fournie, seul le poste "Autre" est disponible
            self.fields['poste'].choices = [('Autre', 'Autre')]

        # Ajustements spécifiques si le formulaire est pour un DRH
        if drh:
            # Ajoute les champs de mot de passe pour l'inscription du DRH
            self.fields['password'] = forms.CharField(widget=forms.PasswordInput(attrs={'class': 'input input-primary w-full', 'placeholder': 'Mot de passe'}), required=True)
            self.fields['password_confirm'] = forms.CharField(widget=forms.PasswordInput(attrs={'class': 'input input-primary w-full', 'placeholder': 'Confirmer le mot de passe'}), required=True)
            # Supprime les champs non pertinents pour un DRH
            if 'drh' in self.fields:
                del self.fields['drh']
            if 'poste' in self.fields:
                del self.fields['poste']
            if 'service' in self.fields:
                del self.fields['service']
        else:
            # Supprime le champ 'drh' si le formulaire n'est pas pour un DRH
            if 'drh' in self.fields:
                del self.fields['drh']

    # Méthode de nettoyage spécifique pour le champ 'email'
    def clean_email(self):
        email = self.cleaned_data.get('email')
        # Vérifie si l'email est déjà utilisé par un autre employé (sauf l'employé actuel en cas de modification)
        if Employe.objects.filter(email=email).exclude(pk=self.instance.pk).exists():
            raise forms.ValidationError("Un autre employé utilise déjà cette adresse email.")
        return email
    
    # Méthode de nettoyage générale pour valider l'ensemble du formulaire
    def clean(self):
        cleaned_data = super().clean() # Appelle la méthode clean de la classe parente
        poste = cleaned_data.get('poste')
        poste_autre = cleaned_data.get('poste_autre')

        # Gère le cas où "Autre" est sélectionné pour le poste
        if poste == 'Autre':
            if not poste_autre:
                self.add_error('poste_autre', "Veuillez préciser le poste.")
            else:
                cleaned_data['poste'] = poste_autre
        
        password = cleaned_data.get("password")
        password_confirm = cleaned_data.get("password_confirm")

        # Valide la correspondance des mots de passe si présents
        if password and password_confirm:
            if password != password_confirm:
                raise forms.ValidationError(
                    "Les deux mots de passe ne correspondent pas."
                )
        return cleaned_data

    # Méthode de sauvegarde personnalisée pour créer un utilisateur Django si un mot de passe est fourni
    def save(self, commit=True):
        employe = super().save(commit=False) # Sauvegarde l'instance de l'employé sans la persister

        # Si un mot de passe est fourni (cas d'inscription d'un nouvel employé/DRH)
        if 'password' in self.cleaned_data:
            # Crée un nouvel utilisateur Django
            user = User.objects.create_user(
                username=self.cleaned_data['email'], # L'email est utilisé comme nom d'utilisateur
                email=self.cleaned_data['email'],
                password=self.cleaned_data['password']
            )
            employe.utilisateur = user # Associe l'utilisateur créé à l'employé

        if commit:
            employe.save() # Sauvegarde l'employé dans la base de données
        return employe
