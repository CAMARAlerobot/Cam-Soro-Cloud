from django.db import models
from django.contrib.auth.models import User

class Menu(models.Model):
    name = models.CharField(max_length=100)          # Nom du plat
    description = models.TextField(blank=True)       # Description du plat
    price = models.DecimalField(max_digits=6, decimal_places=2)  # Prix du plat
    image = models.ImageField(upload_to='images/', blank=True, null=True)  # Image du plat (optionnelle)

    def __str__(self):
        return self.name
    
class DailySpecial(models.Model):
    date = models.DateField()
    menu = models.ForeignKey(Menu, on_delete=models.CASCADE)
    
    def __str__(self):
        return self.menu.name

class Commande(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='commandes')
    plats = models.ManyToManyField(Menu, through='CommandeDetail')
    date_commande = models.DateTimeField(auto_now_add=True)
    statut = models.CharField(max_length=20, choices=[
        ('en_cours', 'En cours'),
        ('livree', 'Livrée'),
        ('annulee', 'Annulée'),
    ], default='en_cours')

    def __str__(self):
        return f"Commande #{self.id} par {self.user.username}"

class CommandeDetail(models.Model):
    commande = models.ForeignKey(Commande, on_delete=models.CASCADE)
    plat = models.ForeignKey(Menu, on_delete=models.CASCADE)
    quantite = models.PositiveIntegerField(default=1)

    def __str__(self):
        return f"{self.quantite} x {self.plat.name}"
