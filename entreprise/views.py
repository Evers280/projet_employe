from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect, get_object_or_404
from .models import entreprises, services
from .forms import EntrepriseForm, ServiceForm




@login_required
def home(request):
    return render(request, 'entreprise/home.html')


@login_required
def profile_entreprise(request):
    try:
        profile_entreprise = entreprises.objects.get(utilisateur=request.user)
    except entreprises.DoesNotExist:
        profile_entreprise = None
    return render(request, 'entreprise/profile.html', {'entreprise': profile_entreprise})

@login_required
def création_entreprise(request):
    if request.method == 'POST':
        form = EntrepriseForm(request.POST)
        if form.is_valid():
            entreprise = form.save(commit=False)
            entreprise.utilisateur = request.user
            entreprise.save()
            return redirect('profile_entreprise')
    else:
        form = EntrepriseForm()
    
    return render(request, 'entreprise/creation_e.html', {'form': form})
  

@login_required
def modifier_entreprise(request, id):
    entreprise = get_object_or_404(entreprises, id=id)
    
    form = EntrepriseForm(request.POST or None, instance=entreprise)
    if form.is_valid():
        form.save()
        return redirect('profile_entreprise')
    return render(request, 'entreprise/modifier.html', {'form': form, 'entreprise': entreprise})


@login_required
def supprimer_entreprise(request, id):
    entreprise = get_object_or_404(entreprises, id=id)
    if request.method == 'POST':
        entreprise.delete()
        return redirect('profile_entreprise')
    return render(request, 'entreprise/supprimer.html', {'entreprise': entreprise})
  
  
#vues des services
@login_required
def liste_services(request, entreprise_id):
    entreprise = get_object_or_404(entreprises, id=entreprise_id) 
    service_list = services.objects.filter(utilisateur=request.user, entreprise=entreprise)
    return render(request, 'entreprise/services/liste.html', {'services': service_list, 'entreprise': entreprise})
  

@login_required
def creation_service(request, entreprise_id):
    entreprise = get_object_or_404(entreprises, id=entreprise_id)
    
    if request.method == 'POST':
        form = ServiceForm(request.POST)
        if form.is_valid():
            service = form.save(commit=False)
            service.utilisateur = request.user
            service.entreprise = entreprise
            service.save()
            return redirect('liste_services', entreprise_id=entreprise.id)
    else:
        form = ServiceForm()
    
    return render(request, 'entreprise/creation_s.html', {'form': form, 'entreprise': entreprise})
  

@login_required  
def modifier_service(request, entreprise_id, service_id):
    entreprise = get_object_or_404(entreprises, id=entreprise_id)
    service = get_object_or_404(services, id=service_id, entreprise=entreprise)
    
    form = ServiceForm(request.POST or None, instance=service)
    if form.is_valid():
        form.save()
        return redirect('liste_services', entreprise_id=entreprise.id)
    
    return render(request, 'entreprise/services/modifier.html', {'form': form, 'service': service, 'entreprise': entreprise})
  
@login_required
def supprimer_service(request, entreprise_id, service_id):
    entreprise = get_object_or_404(entreprises, id=entreprise_id)
    service = get_object_or_404(services, id=service_id, entreprise=entreprise)
    
    if request.method == 'POST':
        service.delete()
        return redirect('liste_services', entreprise_id=entreprise.id)
    
    return render(request, 'entreprise/services/supprimer.html', {'service': service, 'entreprise': entreprise})  

@login_required
def services_view(request):
    try:
        entreprise = entreprises.objects.get(utilisateur=request.user)
        return redirect('liste_services', entreprise_id=entreprise.id)
    except entreprises.DoesNotExist:
        return render(request, 'entreprise/services.html')