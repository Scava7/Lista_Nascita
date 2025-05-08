from django.shortcuts import render
from .models import Regalo, ImpostazioniPagina

def lista_pubblica(request):
    ordine = request.GET.get('ordine', 'default')

    if ordine == 'disponibili':
        regali = Regalo.objects.order_by('prenotato', 'ordine_default')
    elif ordine == 'alfabetico':
        regali = Regalo.objects.order_by('nome')
    elif ordine == 'prezzo ascendente':
        regali = Regalo.objects.order_by('prezzo')
    elif ordine == 'prezzo discendente':
        regali = Regalo.objects.order_by('-prezzo')
    else:  # default
        regali = Regalo.objects.order_by('ordine_default')

    impostazioni = ImpostazioniPagina.objects.first()
    return render(request, 'lista/lista_pubblica.html', {
        'regali': regali,
        'impostazioni': impostazioni,
        'ordine_attivo': ordine
    })