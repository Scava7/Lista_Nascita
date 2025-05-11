from django.db import models, transaction
from ckeditor.fields import RichTextField

class Regalo(models.Model):
    nome = models.CharField(max_length=100)
    modello = models.CharField(max_length=100, blank=True)
    descrizione = models.TextField(blank=True)
    prenotato = models.BooleanField(default=False)
    immagine = models.ImageField(upload_to='regali/', blank=True, null=True)
    link = models.URLField(blank=True, null=True)
    prezzo = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True)
    ordine_default = models.PositiveIntegerField(default=0)
    prenotato_da = models.ForeignKey('UtenteRegistrato', null=True, blank=True, on_delete=models.SET_NULL
)

    def __str__(self):
        return self.nome

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

        with transaction.atomic():
            # Aggiorna in blocco tutti i record con ordine >= nuovo_valore
            qs.update(ordine_default=models.F('ordine_default') + 1)
    
class ImpostazioniPagina(models.Model):
    titolo = models.CharField(max_length=200, default="Lista Nascita")
    messaggio = RichTextField(blank=True)

    def __str__(self):
        return "Impostazioni Pagina (modifica unica)"
    


class UtenteRegistrato(models.Model):
    nome = models.CharField(max_length=100)
    email = models.EmailField(unique=True)
    data_registrazione = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.nome} ({self.email})"
        

