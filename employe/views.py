from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect, get_object_or_404
from .models import Employe
from .forms import EmployeForm
from rest_framework_simplejwt.views import TokenObtainPairView
from django.contrib.auth import authenticate, login, logout
from django.http import HttpResponseRedirect
from django.urls import reverse
from .forms import LoginForm


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
                return redirect('liste_employes')
            else:
                message = 'Identifiants invalides.'
    return render(request, 'employe/login.html', context={'form': form, 'message': message})



def inscription_employe_drh(request):
    est_drh = True
    
    if request.method == 'POST':
        form = EmployeForm(request.POST, drh=est_drh)
        if form.is_valid():
            employe = form.save(commit=False)
            employe.drh = True
            employe.poste = "DRH"
            employe.save()
            return redirect('liste_employes')
    else:
        form = EmployeForm(drh=est_drh)
    
    context = {'form': form}
    return render(request, 'employe/inscription.html', context)


@login_required
def liste_employes(request):
    employes = Employe.objects.all()
    return render(request, 'employe/liste.html', {'employes': employes})



@login_required
def ajouter_employe(request):  
    
    est_drh = False
    form = EmployeForm(request.POST or None, drh=est_drh)
    if form.is_valid():
        form.save()
        return redirect('liste_employes')
    return render(request, 'employe/formulaire.html', {'form': form})


@login_required
def modifier_employe(request, id):
    employe = get_object_or_404(Employe, id=id)
    est_drh = True  # ou False, selon la logique métier
    form = EmployeForm(request.POST or None, instance=employe, drh=est_drh)
    if form.is_valid():
        form.save()
        return redirect('liste_employes')
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
