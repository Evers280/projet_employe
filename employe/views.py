from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect, get_object_or_404
from .models import Employe
from .forms import EmployeForm
from rest_framework_simplejwt.views import TokenObtainPairView
from django.contrib.auth import authenticate, login, logout
from django.http import HttpResponseRedirect
from django.urls import reverse
from .forms import LoginForm
from entreprise.models import entreprises

def login_page(request):
    form = LoginForm()
    message = ''
    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            user = authenticate(
                username=form.cleaned_data['username'],
                password=form.cleaned_data['password']
            )
            if user is not None:
                login(request, user)
                return redirect('home')
            else:
                message = 'Identifiants invalides.'
    return render(request, 'employe/login.html', context={'form': form, 'message': message})

def inscription_employe_drh(request):
    est_drh = True
    
    if request.method == 'POST':
        # The `entreprise` is not available here. The form will have limited `poste` choices.
        # This might need to be addressed depending on the user flow.
        form = EmployeForm(request.POST, drh=est_drh)
        if form.is_valid():
            employe = form.save(commit=False)
            employe.drh = True
            employe.poste = "DRH"
            employe.save()
            login(request, employe.utilisateur)
            return redirect('home')
    else:
        form = EmployeForm(drh=est_drh)
    
    context = {'form': form}
    return render(request, 'employe/inscription.html', context)

@login_required
def liste_employes(request):
    try:
        entreprise = entreprises.objects.get(utilisateur=request.user)
        employes = Employe.objects.filter(utilisateur=request.user)
        return render(request, 'employe/liste.html', {'employes': employes, 'entreprise_existe': True})
    except entreprises.DoesNotExist:
        return render(request, 'employe/liste.html', {'entreprise_existe': False})

@login_required
def ajouter_employe(request):
    try:
        entreprise = entreprises.objects.get(utilisateur=request.user)
    except entreprises.DoesNotExist:
        return redirect('home') # Or some other appropriate action

    est_drh = False
    if request.method == 'POST':
        form = EmployeForm(request.POST, drh=est_drh, entreprise=entreprise)
        if form.is_valid():
            employe = form.save(commit=False)
            employe.utilisateur = request.user
            form.save()
            return redirect('liste_employes')
    else:
        form = EmployeForm(drh=est_drh, entreprise=entreprise)
        
    return render(request, 'employe/formulaire.html', {'form': form})

@login_required
def modifier_employe(request, id):
    employe = get_object_or_404(Employe, id=id)
    try:
        entreprise = employe.service.entreprise
    except AttributeError:
        try:
            entreprise = entreprises.objects.get(utilisateur=employe.utilisateur)
        except entreprises.DoesNotExist:
            return redirect('home')

    est_drh = False # Should not be DRH form here
    if request.method == 'POST':
        form = EmployeForm(request.POST, instance=employe, drh=est_drh, entreprise=entreprise)
        if form.is_valid():
            form.save()
            return redirect('liste_employes')
    else:
        form = EmployeForm(instance=employe, drh=est_drh, entreprise=entreprise)

    return render(request, 'employe/formulaire.html', {'form': form})

@login_required
def supprimer_employe(request, id):
    employe = get_object_or_404(Employe, id=id)
    if request.method == 'POST':
        employe.delete()
        return redirect('liste_employes')
    return render(request, 'employe/confirmer_suppression.html', {'employe': employe})

def logout_view(request):
    logout(request)
    return redirect('login')