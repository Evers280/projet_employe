"""
Configuration des URLs pour le projet 'projet_employe'.

Ce fichier définit les routes principales de l'application web.
Chaque 'path' associe une URL à une vue (fonction ou classe) ou inclut les URLs d'une autre application.
"""
from django.contrib import admin
from django.urls import path, include

# Importations nécessaires pour la documentation Swagger/OpenAPI
from rest_framework import permissions
from drf_yasg.views import get_schema_view
from drf_yasg import openapi


# Configuration du schéma Swagger/OpenAPI
# Cela définit les métadonnées de votre API qui seront affichées dans la documentation.
schema_view = get_schema_view(
   openapi.Info(
      title="Projet Employe API",  # Titre de votre API
      default_version='v1',       # Version de l'API
      description="Documentation de l'API pour le Projet Employe", # Description de l'API
      terms_of_service="https://www.google.com/policies/terms/", # Conditions d'utilisation (optionnel)
      contact=openapi.Contact(email="contact@projetemploye.local"), # Contact pour l'API
      license=openapi.License(name="BSD License"), # Licence de l'API
   ),
   public=True,  # Rend la documentation accessible publiquement
   permission_classes=(permissions.AllowAny,), # Permet à tout le monde d'accéder à la documentation
)

# Liste des patterns d'URL du projet
urlpatterns = [
    # URL pour l'interface d'administration de Django
    path('admin/', admin.site.urls),

    # Inclusion des URLs des applications spécifiques
    # Les URLs de l'application 'employe' sont incluses ici.
    path('', include('employe.urls')),
    # Les URLs de l'application 'entreprise' sont incluses ici.
    path('entreprise/', include('entreprise.urls')),

    # URLs pour la documentation Swagger/OpenAPI
    # Accès à l'interface utilisateur Swagger UI
    path('swagger/', schema_view.with_ui('swagger', cache_timeout=0), name='schema-swagger-ui'),
    # Accès à l'interface utilisateur ReDoc
    path('redoc/', schema_view.with_ui('redoc', cache_timeout=0), name='schema-redoc'),
]
