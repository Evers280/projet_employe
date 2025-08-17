from django.urls import path
from . import views

urlpatterns = [
    path("", views.home, name='home'),
    path("profile de l'entreprise/", views.profile_entreprise, name='profile_entreprise'),
    path("creation d'une entreprise/", views.création_entreprise, name='creation_entreprise'),
    path("modifier le profile de l'entreprise/<int:id>/", views.modifier_entreprise, name='modifier_entreprise'),
    path("supprimer l'entreprise/<int:id>/", views.supprimer_entreprise, name='supprimer_entreprise'),
   
    path("services/", views.services_view, name='services_view'),
   
    # URLs pour les services
    path("liste des services/<int:entreprise_id>/", views.liste_services, name='liste_services'),
    path("creation d'un service/<int:entreprise_id>/", views.creation_service, name='creation_service'),
    path("modifier un service/<int:entreprise_id>/<int:service_id>/", views.modifier_service, name='modifier_service'),
    path("supprimer un service/<int:entreprise_id>/<int:service_id>/", views.supprimer_service, name='supprimer_service'),
] 