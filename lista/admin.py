from django.contrib import admin
from .models import Regalo, ImpostazioniPagina

admin.site.register(Regalo)

@admin.register(ImpostazioniPagina)
class ImpostazioniPaginaAdmin(admin.ModelAdmin):
    def has_add_permission(self, request):
        # Permette l'aggiunta solo se non esiste già
        return not ImpostazioniPagina.objects.exists()