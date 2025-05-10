from django.contrib import admin
from .models import Regalo, ImpostazioniPagina, UtenteRegistrato

class UtenteRegistratoAdmin(admin.ModelAdmin):
    list_display = ['nome', 'email', 'data_registrazione']



admin.site.register(UtenteRegistrato, UtenteRegistratoAdmin)

@admin.register(ImpostazioniPagina)
class ImpostazioniPaginaAdmin(admin.ModelAdmin):
    def has_add_permission(self, request):
        # Permette l'aggiunta solo se non esiste già
        return not ImpostazioniPagina.objects.exists()
    

@admin.action(description="Sblocca i regali con prenotazioni invalide o orfane")
def sblocca_regali_invalidi(modeladmin, request, queryset):
    orfani = 0
    for regalo in queryset:
        if regalo.prenotato:
            # Se non esiste prenotato_da oppure non è più presente nel DB, resetta
            if not regalo.prenotato_da or not UtenteRegistrato.objects.filter(pk=regalo.prenotato_da_id).exists():
                regalo.prenotato = False
                regalo.prenotato_da = None
                regalo.save()
                orfani += 1
    modeladmin.message_user(request, f"{orfani} regali sbloccati.")

@admin.register(Regalo)
class RegaloAdmin(admin.ModelAdmin):
    list_display = ['nome', 'prenotato', 'prenotato_da']
    actions = [sblocca_regali_invalidi]