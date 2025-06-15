from django.urls import path
from . import views

app_name = 'app'  # adapte selon le nom de ton app

urlpatterns = [
    path('', views.home, name='home'),  # Page d’accueil
    path('menu/', views.menu_list, name='menu_list'),               # Page d’accueil - liste des plats
    path('menu/<int:pk>/', views.menu_detail, name='menu_detail'),  # Détail d’un plat

    path('commande/create/', views.commande_create, name='commande_create'),  # Créer une commande
    path('commandes/', views.commande_list, name='commande_list'),           # Liste des commandes utilisateur
    path('commande/<int:pk>/', views.commande_detail, name='commande_detail'),  # Détail d’une commande

    path('profile/', views.profile, name='profile'),  # Page profil utilisateur (infos + commandes)
]
