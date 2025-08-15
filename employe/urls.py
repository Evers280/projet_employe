from django.urls import path
from .import views 
from rest_framework_simplejwt.views import (
    TokenRefreshView,
)

urlpatterns = [
    path('', views.liste_employes, name='liste_employes'),  # URL pour la liste des employés  
    path('inscription/', views.inscription_employe_drh, name='inscription_employe_drh'), 
    path('ajouter/', views.ajouter_employe, name='ajouter_employe'),   # URL pour ajouter un employé
    path('modifier/<int:id>/', views.modifier_employe, name='modifier_employe'),  # URL pour modifier un employé
    path('supprimer/<int:id>/', views.supprimer_employe, name='supprimer_employe'),  # URL pour supprimer un employé
    path('login/', views.login_page, name='login'),
    path('Gestploided/token/', views.LoginView.as_view(), name='token_obtain_pair'),
    path('apGestploided/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
]
