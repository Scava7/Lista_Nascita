from django.contrib import admin
from .models import Regalo, ImpostazioniPagina, UtenteRegistrato

class UtenteRegistratoAdmin(admin.ModelAdmin):
    list_display = ['nome', 'email', 'data_registrazione']

admin.site.register(Regalo)

admin.site.register(UtenteRegistrato, UtenteRegistratoAdmin)

@admin.register(ImpostazioniPagina)
class ImpostazioniPaginaAdmin(admin.ModelAdmin):
    def has_add_permission(self, request):
        # Permette l'aggiunta solo se non esiste già
        return not ImpostazioniPagina.objects.exists()