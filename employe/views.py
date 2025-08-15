from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect, get_object_or_404
from .models import Employe
from .forms import EmployeForm
from rest_framework_simplejwt.views import TokenObtainPairView
from django.contrib.auth import authenticate, login
from django.http import HttpResponseRedirect
from django.urls import reverse
from .forms import LoginForm

class LoginView(TokenObtainPairView):
    template_name = 'employe/login.html'

    def post(self, request, *args, **kwargs):
        response = super().post(request, *args, **kwargs)
        if response.status_code == 200:
            # The user is authenticated by DRF, you can now log them in to Django's session.
            # Note: this part is tricky because TokenObtainPairView does not return the user object.
            # We need to re-authenticate to get the user object.
            # This is not ideal, but it's a common approach.
            user = authenticate(username=request.data['username'], password=request.data['password'])
            if user is not None:
                login(request, user)
                # Redirect to a success page.
                return HttpResponseRedirect(reverse('liste_employes'))
        return response

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
    return render(request, 'employe/formulaire.html', context)


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