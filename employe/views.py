from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect, get_object_or_404
from .models import Employe
from .forms import EmployeForm
# from rest_framework_simplejwt.views import TokenObtainPairView # Commenté car JWT a été supprimé
from django.contrib.auth import authenticate, login, logout
from django.http import HttpResponseRedirect
from django.urls import reverse
from .forms import LoginForm
from entreprise.models import entreprises

# Vue pour la page de connexion des utilisateurs
def login_page(request):
    form = LoginForm()  # Instancie le formulaire de connexion
    message = ''        # Message d'erreur ou de succès
    if request.method == 'POST':
        form = LoginForm(request.POST) # Remplit le formulaire avec les données POST
        if form.is_valid():
            # Tente d'authentifier l'utilisateur avec les identifiants fournis
            user = authenticate(
                username=form.cleaned_data['username'],
                password=form.cleaned_data['password']
            )
            if user is not None:
                login(request, user) # Connecte l'utilisateur
                return redirect('home') # Redirige vers la page d'accueil après connexion réussie
            else:
                message = 'Identifiants invalides.' # Message en cas d'échec d'authentification
    # Affiche la page de connexion avec le formulaire et un message éventuel
    return render(request, 'employe/login.html', context={'form': form, 'message': message})

# Vue pour l'inscription d'un employé avec le rôle de DRH
def inscription_employe_drh(request):
    est_drh = True # Indique que cet employé sera un DRH
    
    if request.method == 'POST':
        # Crée une instance du formulaire EmployeForm avec les données POST
        # Le paramètre `drh=est_drh` est passé au formulaire pour ajuster son comportement
        form = EmployeForm(request.POST, drh=est_drh)
        if form.is_valid():
            employe = form.save(commit=False) # Sauvegarde l'employé sans le persister immédiatement
            employe.drh = True # Définit explicitement l'employé comme DRH
            employe.poste = "DRH" # Attribue le poste de DRH
            employe.save() # Sauvegarde l'employé dans la base de données
            login(request, employe.utilisateur) # Connecte l'utilisateur associé à l'employé
            return redirect('home') # Redirige vers la page d'accueil
    else:
        # Affiche un formulaire vide pour l'inscription du DRH
        form = EmployeForm(drh=est_drh)
    
    context = {'form': form}
    return render(request, 'employe/inscription.html', context)

# Vue pour l'inscription d'un employé avec le rôle de DRH
def inscription_employe_drh(request):
    est_drh = True # Indique que cet employé sera un DRH
    
    if request.method == 'POST':
        # Crée une instance du formulaire EmployeForm avec les données POST
        # Le paramètre `drh=est_drh` est passé au formulaire pour ajuster son comportement
        form = EmployeForm(request.POST, drh=est_drh)
        if form.is_valid():
            employe = form.save(commit=False) # Sauvegarde l'employé sans le persister immédiatement
            employe.drh = True # Définit explicitement l'employé comme DRH
            employe.poste = "DRH" # Attribue le poste de DRH
            employe.save() # Sauvegarde l'employé dans la base de données
            login(request, employe.utilisateur) # Connecte l'utilisateur associé à l'employé
            return redirect('home') # Redirige vers la page d'accueil
    else:
        # Affiche un formulaire vide pour l'inscription du DRH
        form = EmployeForm(drh=est_drh)
    
    context = {'form': form}
    return render(request, 'employe/inscription.html', context)

# Vue pour lister les employés, accessible uniquement aux utilisateurs connectés
@login_required
def liste_employes(request):
    try:
        # Tente de récupérer l'entreprise associée à l'utilisateur connecté
        entreprise = entreprises.objects.get(utilisateur=request.user)
        # Récupère tous les employés associés à l'utilisateur (ou à l'entreprise de l'utilisateur)
        employes = Employe.objects.filter(utilisateur=request.user)
        # Affiche la liste des employés
        return render(request, 'employe/liste.html', {'employes': employes, 'entreprise_existe': True})
    except entreprises.DoesNotExist:
        # Si aucune entreprise n'est trouvée pour l'utilisateur, affiche un message approprié
        return render(request, 'employe/liste.html', {'entreprise_existe': False})

# Vue pour ajouter un nouvel employé, accessible uniquement aux utilisateurs connectés
@login_required
def ajouter_employe(request):
    try:
        # Récupère l'entreprise de l'utilisateur connecté
        entreprise = entreprises.objects.get(utilisateur=request.user)
    except entreprises.DoesNotExist:
        # Redirige si l'entreprise n'existe pas (nécessaire pour ajouter un employé)
        return redirect('home') 

    est_drh = False # Indique que ce n'est pas un formulaire pour DRH
    if request.method == 'POST':
        # Crée une instance du formulaire EmployeForm avec les données POST
        form = EmployeForm(request.POST, drh=est_drh, entreprise=entreprise)
        if form.is_valid():
            employe = form.save(commit=False) # Sauvegarde l'employé sans le persister immédiatement
            employe.utilisateur = request.user # Associe l'employé à l'utilisateur connecté
            form.save() # Sauvegarde l'employé dans la base de données
            return redirect('liste_employes') # Redirige vers la liste des employés
    else:
        # Affiche un formulaire vide pour ajouter un employé
        form = EmployeForm(drh=est_drh, entreprise=entreprise)
        
    return render(request, 'employe/formulaire.html', {'form': form})

# Vue pour modifier un employé existant, accessible uniquement aux utilisateurs connectés
@login_required
def modifier_employe(request, id):
    # Récupère l'employé à modifier ou renvoie une erreur 404
    employe = get_object_or_404(Employe, id=id)
    try:
        # Tente de récupérer l'entreprise via le service de l'employé
        entreprise = employe.service.entreprise
    except AttributeError:
        try:
            # Si le service n'a pas d'entreprise, tente de récupérer l'entreprise via l'utilisateur de l'employé
            entreprise = entreprises.objects.get(utilisateur=employe.utilisateur)
        except entreprises.DoesNotExist:
            # Redirige si l'entreprise n'est pas trouvée
            return redirect('home')

    est_drh = False # Ce n'est pas un formulaire pour DRH
    if request.method == 'POST':
        # Crée une instance du formulaire EmployeForm avec les données POST et l'instance de l'employé
        form = EmployeForm(request.POST, instance=employe, drh=est_drh, entreprise=entreprise)
        if form.is_valid():
            form.save() # Sauvegarde les modifications de l'employé
            return redirect('liste_employes') # Redirige vers la liste des employés
    else:
        # Affiche le formulaire pré-rempli avec les données de l'employé
        form = EmployeForm(instance=employe, drh=est_drh, entreprise=entreprise)

    return render(request, 'employe/formulaire.html', {'form': form})

# Vue pour supprimer un employé, accessible uniquement aux utilisateurs connectés
@login_required
def supprimer_employe(request, id):
    # Récupère l'employé à supprimer ou renvoie une erreur 404
    employe = get_object_or_404(Employe, id=id)
    if request.method == 'POST':
        employe.delete() # Supprime l'employé de la base de données
        return redirect('liste_employes') # Redirige vers la liste des employés
    # Affiche la page de confirmation de suppression
    return render(request, 'employe/confirmer_suppression.html', {'employe': employe})

# Vue pour la déconnexion de l'utilisateur
def logout_view(request):
    logout(request) # Déconnecte l'utilisateur
    return redirect('login') # Redirige vers la page de connexion
