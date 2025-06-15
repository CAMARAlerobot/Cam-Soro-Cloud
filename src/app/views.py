from django.shortcuts import render, get_object_or_404, redirect
from .models import Menu, Commande, CommandeDetail
from django.contrib.auth.decorators import login_required

from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib import messages

# Inscription
def register_view(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, "Votre compte a été créé avec succès. Vous pouvez vous connecter.")
            return redirect('app:login')
    else:
        form = UserCreationForm()
    return render(request, 'app/register.html', {'form': form})

# Connexion
def login_view(request):
    if request.method == 'POST':
        form = AuthenticationForm(request=request, data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            messages.success(request, f"Bienvenue {user.username} !")
            return redirect('app:home')
    else:
        form = AuthenticationForm()
    return render(request, 'app/login.html', {'form': form})

# Déconnexion
def logout_view(request):
    logout(request)
    messages.info(request, "Vous êtes déconnecté.")
    return redirect('app:login')

def home(request):
    return render(request, 'app/home.html')

def menu_list(request):
    plats = Menu.objects.all()
    return render(request, 'app/menu_list.html', {'plats': plats})

def menu_detail(request, pk):
    plat = get_object_or_404(Menu, pk=pk)
    return render(request, 'app/menu_detail.html', {'plat': plat})

@login_required
def commande_create(request):
    # Ici on ferait un formulaire (à créer) pour commander des plats
    # Simplification : commande avec un seul plat pour exemple
    if request.method == 'POST':
        plat_id = request.POST.get('plat_id')
        quantite = int(request.POST.get('quantite', 1))
        plat = get_object_or_404(Menu, id=plat_id)

        commande = Commande.objects.create(user=request.user)
        CommandeDetail.objects.create(commande=commande, plat=plat, quantite=quantite)

        return redirect('app:commande_detail', pk=commande.pk)

    plats = Menu.objects.all()
    return render(request, 'app/commande_create.html', {'plats': plats})

@login_required
def commande_list(request):
    commandes = Commande.objects.filter(user=request.user).order_by('-date_commande')
    return render(request, 'app/commande_list.html', {'commandes': commandes})

@login_required
def commande_detail(request, pk):
    commande = get_object_or_404(Commande, pk=pk, user=request.user)
    details = commande.commandedetail_set.all()
    for detail in details:
        detail.total = detail.quantite * detail.plat.price

    return render(request, 'app/commande_detail.html', {'commande': commande, 'details': details})

@login_required
def profile(request):
    commandes = Commande.objects.filter(user=request.user).order_by('-date_commande')
    return render(request, 'app/profile.html', {'commandes': commandes})
