from django.db import models
from django.contrib.auth.models import User

class Employe(models.Model):
    
    SEXE_CHOICES = [
        ('M', 'Masculin'),
        ('F', 'Féminin'),
    ]
    
    # Relation OneToOne avec le modèle User de Django
    utilisateur = models.ForeignKey(User, on_delete=models.CASCADE)
    
    
    nom = models.CharField(max_length=100)
    prenom = models.CharField(max_length=100)
    age = models.PositiveIntegerField(default=25)
    sexe = models.CharField(max_length=10, choices=[('M', 'Masculin'), ('F', 'Féminin')])
    email = models.EmailField(unique=True)
    numero_telephone = models.CharField(max_length=15, unique=True)
    poste = models.CharField(max_length=100)
    salaire = models.DecimalField(max_digits=10, decimal_places=2)
    date_embauche = models.DateField(auto_now_add=True)
    drh = models.CharField(max_length=50, default=False)
    
    def __str__(self):
        return f"{self.prenom} {self.nom} - {self.poste}"  
