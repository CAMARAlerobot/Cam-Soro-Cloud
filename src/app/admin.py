from django.contrib import admin
from django.utils.html import format_html
from django.utils import timezone
from .models import Menu, Commande, CommandeDetail, DailySpecial

@admin.register(Menu)
class MenuAdmin(admin.ModelAdmin):
    list_display = ('name', 'price', 'is_today_special')
    search_fields = ('name',)
    actions = ['set_as_today_special']

    def is_today_special(self, obj):
        today = timezone.now().date()
        return DailySpecial.objects.filter(menu=obj, date=today).exists()
    is_today_special.boolean = True
    is_today_special.short_description = "Plat du jour"

    def set_as_today_special(self, request, queryset):
        today = timezone.now().date()
        DailySpecial.objects.filter(date=today).delete()  # On efface les anciens plats du jour
        for menu in queryset:
            DailySpecial.objects.create(menu=menu, date=today)
        self.message_user(request, "Plat(s) du jour mis à jour avec succès.")
    set_as_today_special.short_description = "Définir comme plat du jour pour aujourd'hui"


class CommandeDetailInline(admin.TabularInline):
    model = CommandeDetail
    extra = 1


@admin.register(Commande)
class CommandeAdmin(admin.ModelAdmin):
    list_display = ('id', 'user', 'date_commande', 'statut', 'view_details')
    list_filter = ('statut', 'date_commande')
    search_fields = ('user__username',)
    inlines = [CommandeDetailInline]
    actions = ['marquer_livree', 'marquer_annulee', 'remettre_en_cours']

    def view_details(self, obj):
        return format_html('<a href="/admin/app/commande/{}/change/">Détails</a>', obj.id)
    view_details.short_description = "Voir"

    def marquer_livree(self, request, queryset):
        updated = queryset.update(statut='livree')
        self.message_user(request, f"{updated} commande(s) marquée(s) comme livrée(s).")
    marquer_livree.short_description = "Marquer comme livrée"

    def marquer_annulee(self, request, queryset):
        updated = queryset.update(statut='annulee')
        self.message_user(request, f"{updated} commande(s) annulée(s).")
    marquer_annulee.short_description = "Marquer comme annulée"

    def remettre_en_cours(self, request, queryset):
        updated = queryset.update(statut='en_cours')
        self.message_user(request, f"{updated} commande(s) remise(s) en cours.")
    remettre_en_cours.short_description = "Remettre en cours"
