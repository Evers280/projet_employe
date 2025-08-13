from django.db import models

class Employe(models.Model):
    nom = models.CharField(max_length=100)
    prenom = models.CharField(max_length=100)
    email = models.EmailField()
    poste = models.CharField(max_length=100)
    salaire = models.DecimalField(max_digits=10, decimal_places=2)
    
    def __str__(self):
        return f"{self.prenom} {self.nom} - {self.poste}"  
