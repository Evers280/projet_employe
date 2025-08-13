from django.urls import path
from .import views 

urlpatterns = [
    path('', views.liste_employes, name='liste_employes'),  # URL pour la liste des employés   
    path('ajouter/', views.ajouter_employe, name='ajouter_employe'),   # URL pour ajouter un employé
    path('modifier/<int:id>/', views.modifier_employe, name='modifier_employe'),  # URL pour modifier un employé
    path('supprimer/<int:id>/', views.supprimer_employe, name='supprimer_employe'),  # URL pour supprimer un employé
]
