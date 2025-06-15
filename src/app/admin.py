from django.contrib import admin
from .models import Menu, Commande, CommandeDetail

@admin.register(Menu)
class MenuAdmin(admin.ModelAdmin):
    list_display = ('name', 'price')
    search_fields = ('name',)

class CommandeDetailInline(admin.TabularInline):
    model = CommandeDetail
    extra = 1

@admin.register(Commande)
class CommandeAdmin(admin.ModelAdmin):
    list_display = ('id', 'user', 'date_commande', 'statut')
    list_filter = ('statut', 'date_commande')
    search_fields = ('user__username',)
    inlines = [CommandeDetailInline]
