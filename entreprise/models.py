from django.db import models
from django.contrib.auth.models import User
from employe.models import *
from django.db.models.signals import post_save, pre_save
from django.dispatch import receiver

SERVICES_PAR_SECTEUR = {
    'Industrie': [
        "Production/Opérations",
        "Recherche et Développement (R&D)",
        "Logistique",
        "Qualité",
        "Maintenance",
        "Sécurité/Environnement",
    ],
    'Services': [
        "Commercial/Ventes",
        "Marketing & Communication",
        "Support Client",
        "Informatique/IT",
        "Conseil/Expertise",
    ],
    'Commerce': [
        "Achats",
        "Ventes/Magasin",
        "Merchandising",
        "Gestion de la chaîne d'approvisionnement",
    ],
    'Agriculture': [
        "Production agricole",
        "Exploitation/Maintenance",
        "Recherche agronomique",
        "Commercialisation",
    ],
    'BTP': [
        "Études/Bureau d'études",
        "Conduite de travaux",
        "Matériel et Logistique",
        "Sécurité du travail",
    ],
}

SERVICES_COMMUNS = [
    "Ressources Humaines (RH)",
    "Comptabilité/Finance",
    "Direction Générale",
    "Juridique",
]

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
        return f"{self.nom_entreprise} - {self.adresse_siege} -{self.secteur_activite}"


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

def _creer_services_pour_entreprise(instance):
    secteur = instance.secteur_activite
    services_a_creer = SERVICES_PAR_SECTEUR.get(secteur, [])
    tous_les_services = services_a_creer + SERVICES_COMMUNS

    for i, nom_service in enumerate(tous_les_services):
        numero_service = f"SRV-{instance.id}-{i+1}"
        email_service = f"contact-service-{instance.id}-{i+1}@{instance.nom_entreprise.lower().replace(' ', '')}.com"

        services.objects.create(
            entreprise=instance,
            utilisateur=instance.utilisateur,
            nom_service=nom_service,
            numero_service=numero_service,
            email_service=email_service,
            budget_annuel=0,
            objectifs_service="Objectifs à définir."
        )

@receiver(pre_save, sender=entreprises)
def store_original_secteur(sender, instance, **kwargs):
    if instance.pk:
        try:
            instance._original_secteur_activite = entreprises.objects.get(pk=instance.pk).secteur_activite
        except entreprises.DoesNotExist:
            instance._original_secteur_activite = None

@receiver(post_save, sender=entreprises)
def creer_ou_maj_services_par_defaut(sender, instance, created, **kwargs):
    if created:
        _creer_services_pour_entreprise(instance)
    else:
        original_secteur = getattr(instance, '_original_secteur_activite', None)
        if original_secteur is not None and original_secteur != instance.secteur_activite:
            instance.services.all().delete()
            _creer_services_pour_entreprise(instance)