from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect, get_object_or_404
from .models import entreprises, services
from .forms import EntrepriseForm, ServiceForm
from employe.models import Employe

# Vue pour la page d'accueil de l'application entreprise.
# Nécessite que l'utilisateur soit connecté.
@login_required
def home(request):
    # Vérifie si l'utilisateur connecté a déjà une entreprise associée.
    has_enterprise = entreprises.objects.filter(utilisateur=request.user).exists()
    # Rend la page d'accueil avec l'information sur l'existence d'une entreprise.
    return render(request, 'entreprise/home.html', {'has_enterprise': has_enterprise})

# Vue pour afficher le profil de l'entreprise de l'utilisateur connecté.
# Nécessite que l'utilisateur soit connecté.
@login_required
def profile_entreprise(request):
    try:
        # Tente de récupérer l'entreprise associée à l'utilisateur actuel.
        profile_entreprise = entreprises.objects.get(utilisateur=request.user)
    except entreprises.DoesNotExist:
        # Si aucune entreprise n'est trouvée, définit profile_entreprise à None.
        profile_entreprise = None
    # Rend la page de profil de l'entreprise.
    return render(request, 'entreprise/profile.html', {'entreprise': profile_entreprise})

# Vue pour la création d'une nouvelle entreprise.
# Nécessite que l'utilisateur soit connecté.
@login_required
def création_entreprise(request):
    if request.method == 'POST':
        # Si la requête est de type POST, traite les données du formulaire.
        form = EntrepriseForm(request.POST)
        if form.is_valid():
            # Si le formulaire est valide, sauvegarde l'entreprise mais ne la committe pas encore.
            entreprise = form.save(commit=False)
            # Associe l'entreprise à l'utilisateur actuel.
            entreprise.utilisateur = request.user
            # Sauvegarde l'entreprise dans la base de données.
            entreprise.save()

            try:
                # Tente de récupérer l'employé DRH associé à l'utilisateur.
                drh_employe = Employe.objects.get(utilisateur=request.user)
                # Tente de récupérer le service "Ressources Humaines (RH)" pour cette entreprise.
                rh_service = services.objects.get(entreprise=entreprise, nom_service="Ressources Humaines (RH)")
                # Associe l'employé DRH au service RH.
                drh_employe.service = rh_service
                # Sauvegarde les modifications de l'employé DRH.
                drh_employe.save(update_fields=['service'])
            except (Employe.DoesNotExist, services.DoesNotExist):
                # Ignore l'erreur si l'employé DRH ou le service RH n'existe pas.
                pass

            # Redirige vers la page de profil de l'entreprise après la création.
            return redirect('profile_entreprise')
    else:
        # Si la requête n'est pas POST, affiche un formulaire vide.
        form = EntrepriseForm()
    
    # Rend la page de création d'entreprise avec le formulaire.
    return render(request, 'entreprise/creation_e.html', {'form': form})
  
# Vue pour modifier une entreprise existante.
# Nécessite que l'utilisateur soit connecté.
@login_required
def modifier_entreprise(request, id):
    # Récupère l'entreprise par son ID, ou renvoie une erreur 404 si non trouvée.
    entreprise = get_object_or_404(entreprises, id=id)
    
    # Initialise le formulaire avec les données de la requête ou l'instance de l'entreprise.
    form = EntrepriseForm(request.POST or None, instance=entreprise)
    if form.is_valid():
        # Si le formulaire est valide, sauvegarde les modifications.
        form.save()
        # Redirige vers la page de profil de l'entreprise.
        return redirect('profile_entreprise')
    # Rend la page de modification d'entreprise avec le formulaire et l'entreprise.
    return render(request, 'entreprise/modifier.html', {'form': form, 'entreprise': entreprise})

# Vue pour supprimer une entreprise existante.
# Nécessite que l'utilisateur soit connecté.
@login_required
def supprimer_entreprise(request, id):
    # Récupère l'entreprise par son ID, ou renvoie une erreur 404 si non trouvée.
    entreprise = get_object_or_404(entreprises, id=id)
    if request.method == 'POST':
        # Si la requête est de type POST, supprime l'entreprise.
        entreprise.delete()
        # Redirige vers la page de profil de l'entreprise.
        return redirect('profile_entreprise')
    # Rend la page de confirmation de suppression d'entreprise.
    return render(request, 'entreprise/supprimer.html', {'entreprise': entreprise})
  
# Vues des services

# Vue pour lister tous les services associés à l'entreprise de l'utilisateur connecté.
# Nécessite que l'utilisateur soit connecté.
@login_required
def liste_services(request):
    # Vérifie si l'utilisateur a une entreprise.
    entreprise_existe = entreprises.objects.filter(utilisateur=request.user).exists()
    if entreprise_existe:
        # Si une entreprise existe, récupère l'entreprise et les services associés.
        entreprise = entreprises.objects.get(utilisateur=request.user)
        service_list = services.objects.filter(utilisateur=request.user, entreprise=entreprise)
        # Rend la page de liste des services.
        return render(request, 'entreprise/services/liste.html', {'services': service_list, 'entreprise': entreprise, 'entreprise_existe': entreprise_existe})
    else:
        # Si aucune entreprise n'existe, rend la page de liste des services avec l'indication.
        return render(request, 'entreprise/services/liste.html', {'entreprise_existe': entreprise_existe})
  
# Vue pour la création d'un nouveau service pour une entreprise donnée.
# Nécessite que l'utilisateur soit connecté.
@login_required
def creation_service(request, entreprise_id):
    # Récupère l'entreprise par son ID, ou renvoie une erreur 404 si non trouvée.
    entreprise = get_object_or_404(entreprises, id=entreprise_id)
    
    if request.method == 'POST':
        # Si la requête est de type POST, traite les données du formulaire.
        form = ServiceForm(request.POST)
        if form.is_valid():
            # Si le formulaire est valide, sauvegarde le service mais ne le committe pas encore.
            service = form.save(commit=False)
            # Associe le service à l'utilisateur actuel et à l'entreprise.
            service.utilisateur = request.user
            service.entreprise = entreprise
            # Sauvegarde le service dans la base de données.
            service.save()
            # Redirige vers la liste des services de l'entreprise.
            return redirect(reverse('liste_services'))
    else:
        # Si la requête n'est pas POST, affiche un formulaire vide.
        form = ServiceForm()
    
    # Rend la page de création de service avec le formulaire et l'entreprise.
    return render(request, 'entreprise/creation_s.html', {'form': form, 'entreprise': entreprise})
  
# Vue pour modifier un service existant.
# Nécessite que l'utilisateur soit connecté.
@login_required  
def modifier_service(request, entreprise_id, service_id):
    # Récupère l'entreprise et le service par leurs IDs, ou renvoie une erreur 404.
    entreprise = get_object_or_404(entreprises, id=entreprise_id)
    service = get_object_or_404(services, id=service_id, entreprise=entreprise)
    
    # Initialise le formulaire avec les données de la requête ou l'instance du service.
    form = ServiceForm(request.POST or None, instance=service)
    if form.is_valid():
        # Si le formulaire est valide, sauvegarde les modifications.
        form.save()
        # Redirige vers la liste des services de l'entreprise.
        return redirect(reverse('liste_services'))
    
    # Rend la page de modification de service avec le formulaire, le service et l'entreprise.
    return render(request, 'entreprise/services/modifier.html', {'form': form, 'service': service, 'entreprise': entreprise})
  
# Vue pour supprimer un service existant.
# Nécessite que l'utilisateur soit connecté.
@login_required
def supprimer_service(request, entreprise_id, service_id):
    # Récupère l'entreprise et le service par leurs IDs, ou renvoie une erreur 404.
    entreprise = get_object_or_404(entreprises, id=entreprise_id)
    service = get_object_or_404(services, id=service_id, entreprise=entreprise)
    
    if request.method == 'POST':
        # Si la requête est de type POST, supprime le service.
        service.delete()
        # Redirige vers la liste des services de l'entreprise.
        return redirect(reverse('liste_services'))
    
    # Rend la page de confirmation de suppression de service.
    return render(request, 'entreprise/services/supprimer.html', {'service': service, 'entreprise': entreprise})  

# Vue pour rediriger vers la liste des services de l'entreprise de l'utilisateur.
# Nécessite que l'utilisateur soit connecté.
@login_required
def services_view(request):
    try:
        # Tente de récupérer l'entreprise de l'utilisateur.
        entreprise = entreprises.objects.get(utilisateur=request.user)
        # Redirige vers la liste des services de cette entreprise.
        return redirect('liste_services')
    except entreprises.DoesNotExist:
        # Si aucune entreprise n'est trouvée, rend une page générique pour les services.
        return render(request, 'entreprise/services.html')