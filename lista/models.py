from django.db import models

class Regalo(models.Model):
    nome = models.CharField(max_length=100)
    modello = models.CharField(max_length=100, blank=True)
    descrizione = models.TextField(blank=True)
    prenotato = models.BooleanField(default=False)
    immagine = models.ImageField(upload_to='regali/', blank=True, null=True)
    link = models.URLField(blank=True, null=True)
    prezzo = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True)
    ordine_default = models.PositiveIntegerField(default=0)

    def save(self, *args, **kwargs):
        if self.pk:
            # Modifica esistente
            old = Regalo.objects.get(pk=self.pk)
            if self.ordine_default != old.ordine_default:
                self._shift_ordini(self.ordine_default, exclude_id=self.pk)
        else:
            # Nuovo inserimento
            self._shift_ordini(self.ordine_default)

        super().save(*args, **kwargs)

    def _shift_ordini(self, nuovo_valore, exclude_id=None):
        qs = Regalo.objects.filter(ordine_default__gte=nuovo_valore)
        if exclude_id:
            qs = qs.exclude(pk=exclude_id)
        for regalo in qs.order_by('-ordine_default'):
            regalo.ordine_default += 1
            regalo.save()

    def __str__(self):
        return self.nome
    
class ImpostazioniPagina(models.Model):
    titolo = models.CharField(max_length=200, default="Lista Nascita")
    messaggio = models.TextField(blank=True)

    def __str__(self):
        return "Impostazioni Pagina (modifica unica)"