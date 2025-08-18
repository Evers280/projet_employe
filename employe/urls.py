from django.urls import path
from .import views 

# Définition des patterns d'URL pour l'application 'employe'
urlpatterns = [
    # URL pour afficher la liste de tous les employés
    path('liste des employés/', views.liste_employes, name='liste_employes'),  
    # URL pour l'inscription d'un nouvel employé (notamment un DRH)
    path('inscription/', views.inscription_employe_drh, name='inscription_employe_drh'), 
    # URL pour ajouter un nouvel employé
    path('ajouter/', views.ajouter_employe, name='ajouter_employe'),   
    # URL pour modifier les informations d'un employé spécifique (identifié par son ID)
    path('modifier/<int:id>/', views.modifier_employe, name='modifier_employe'),  
    # URL pour supprimer un employé spécifique (identifié par son ID)
    path('supprimer/<int:id>/', views.supprimer_employe, name='supprimer_employe'),  
    # URL de la page de connexion (page d'accueil par défaut de l'application 'employe')
    path('', views.login_page, name='login'),
    # URL pour la déconnexion de l'utilisateur
    path('logout/', views.logout_view, name='logout'),

]
