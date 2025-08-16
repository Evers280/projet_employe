from django.urls import path
from .import views 

urlpatterns = [
    path('liste des employés/', views.liste_employes, name='liste_employes'),  # URL pour la liste des employés  
    path('inscription/', views.inscription_employe_drh, name='inscription_employe_drh'), 
    path('ajouter/', views.ajouter_employe, name='ajouter_employe'),   # URL pour ajouter un employé
    path('modifier/<int:id>/', views.modifier_employe, name='modifier_employe'),  # URL pour modifier un employé
    path('supprimer/<int:id>/', views.supprimer_employe, name='supprimer_employe'),  # URL pour supprimer un employé
    path('', views.login_page, name='login'),
    path('logout/', views.logout_view, name='logout'),

]
