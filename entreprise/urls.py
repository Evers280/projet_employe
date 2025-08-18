from django.urls import path
from . import views

# Définition des motifs d'URL pour l'application 'entreprise'.
urlpatterns = [
    # URL pour la page d'accueil de l'entreprise.
    path("", views.home, name='home'),
    # URL pour afficher le profil de l'entreprise de l'utilisateur.
    path("profile de l'entreprise/", views.profile_entreprise, name='profile_entreprise'),
    # URL pour la création d'une nouvelle entreprise.
    path("creation d'une entreprise/", views.création_entreprise, name='creation_entreprise'),
    # URL pour modifier le profil d'une entreprise existante, identifiée par son ID.
    path("modifier le profile de l'entreprise/<int:id>/", views.modifier_entreprise, name='modifier_entreprise'),
    # URL pour supprimer une entreprise existante, identifiée par son ID.
    path("supprimer l'entreprise/<int:id>/", views.supprimer_entreprise, name='supprimer_entreprise'),
   
    # URL générique pour les services, redirige vers la liste des services de l'entreprise de l'utilisateur.
    path("services/", views.services_view, name='services_view'),
   
    # URLs spécifiques pour la gestion des services.
    # URL pour lister tous les services associés à l'entreprise de l'utilisateur.
    path("liste des services/", views.liste_services, name='liste_services'),
    # URL pour créer un nouveau service pour une entreprise spécifique, identifiée par son ID.
    path("creation d'un service/<int:entreprise_id>/", views.creation_service, name='creation_service'),
    # URL pour modifier un service existant, identifié par l'ID de l'entreprise et l'ID du service.
    path("modifier un service/<int:entreprise_id>/<int:service_id>/", views.modifier_service, name='modifier_service'),
    # URL pour supprimer un service existant, identifié par l'ID de l'entreprise et l'ID du service.
    path("supprimer un service/<int:entreprise_id>/<int:service_id>/", views.supprimer_service, name='supprimer_service'),
]