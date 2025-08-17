from django.db import models
from django.contrib.auth.models import User
from employe.models import *

class entreprises(models.Model):
  
    FORME_JURIDIQUE_CHOICES = [
        ('SARL', 'Société à Responsabilité Limitée'),
        ('SA', 'Société Anonyme'),
        ('SAS', 'Société par Actions Simplifiée'),
        ('EI', 'Entreprise Individuelle'),
        ('EURL', 'Entreprise Unipersonnelle à Responsabilité Limitée')
    ] 

    SECTEUR_ACTIVITE_CHOICES = [
        ('Industrie', 'Industrie'),
        ('Services', 'Services'),
        ('Commerce', 'Commerce'),
        ('Agriculture', 'Agriculture'),
        ('BTP', 'Bâtiment et Travaux Publics')
    ]
    
    utilisateur = models.ForeignKey(User, on_delete=models.CASCADE)
    
    nom_entreprise = models.CharField(max_length=100)
    adresse_siege = models.CharField(max_length=255)
    code_postal = models.CharField(max_length=20, unique=True)
    ville = models.CharField(max_length=100)
    pays = models.CharField(max_length=100)
    telephone_entreprise = models.CharField(max_length=15, unique=True)
    email = models.EmailField(unique=True)
    numero_siret = models.CharField(max_length=14, unique=True)
    code_naf = models.CharField(max_length=5, unique=True)
    forme_juridique = models.CharField(max_length=100, choices=FORME_JURIDIQUE_CHOICES, default='SARL')
    secteur_activite = models.CharField(max_length=100, choices=SECTEUR_ACTIVITE_CHOICES, default='Services')
    nombre_employes = models.PositiveIntegerField()
    date_creation = models.DateField(auto_now_add=True)
    date_derniere_modification = models.DateField(auto_now=True)
    
    id_drh = models.ForeignKey(Employe, on_delete=models.CASCADE, related_name='entreprise_drh', null=True, blank=True)

    def __str__(self):
        return f"{self.nom} - {self.adresse_siege} -{self.secteur_activite}"


class services(models.Model):
    
    entreprise = models.ForeignKey(entreprises, on_delete=models.CASCADE, related_name='services')
    
    utilisateur = models.ForeignKey(User, on_delete=models.CASCADE)
        
    nom_service = models.CharField(max_length=100)
    numero_service = models.CharField(max_length=15, unique=True)
    email_service = models.EmailField(unique=True)
    budget_annuel = models.DecimalField(max_digits=15, decimal_places=2)
    objectifs_service = models.TextField()
    date_creation = models.DateField(auto_now_add=True)
    date_derniere_modification = models.DateField(auto_now=True)

    def __str__(self):
        return f"{self.nom_service} - {self.entreprise.nom_entreprise}"