from django.shortcuts import render, redirect
from .models import Regalo, ImpostazioniPagina, UtenteRegistrato
from .forms import RegistrazioneForm
from django.contrib import messages
from django.shortcuts import get_object_or_404
from .models import Regalo, UtenteRegistrato
from django.views.decorators.http import require_POST

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

    utente = None
    utente_id = request.session.get('utente_id')
    if utente_id:
        try:
            from .models import UtenteRegistrato
            utente = UtenteRegistrato.objects.get(pk=utente_id)
        except UtenteRegistrato.DoesNotExist:
            pass

    impostazioni = ImpostazioniPagina.objects.first()
    return render(request, 'lista/lista_pubblica.html', {
        'regali': regali,
        'impostazioni': impostazioni,
        'ordine_attivo': ordine,
        'utente': utente
    })


def registrazione_utente(request):
    if request.method == 'POST':
        form = RegistrazioneForm(request.POST)
        if form.is_valid():
            utente = form.save()
            request.session['utente_id'] = utente.id  # salva nella sessione
            return redirect('lista_pubblica')  # o dove vuoi portarli dopo
    else:
        form = RegistrazioneForm()
    
    return render(request, 'lista/registrazione.html', {'form': form})


def pagina_utente(request):
    utente_id = request.session.get('utente_id')
    if not utente_id:
        return redirect('registrazione')

    try:
        utente = UtenteRegistrato.objects.get(pk=utente_id)
    except UtenteRegistrato.DoesNotExist:
        return redirect('registrazione')

    regali_prenotati = Regalo.objects.filter(prenotato_da=utente)

    return render(request, 'lista/pagina_utente.html', {
        'utente': utente,
        'regali_prenotati': regali_prenotati
    })


@require_POST
def logout_utente(request):
    request.session.flush()  # elimina tutta la sessione
    return redirect('lista_pubblica')

@require_POST
def prenota_regalo(request, regalo_id):
    utente_id = request.session.get('utente_id')
    if not utente_id:
        messages.error(request, "Devi essere registrato per prenotare.")
        return redirect('registrazione')

    regalo = get_object_or_404(Regalo, pk=regalo_id)
    if regalo.prenotato:
        messages.warning(request, "Questo regalo è già stato prenotato.")
    else:
        regalo.prenotato = True
        regalo.prenotato_da_id = utente_id  # serve campo in modello
        regalo.save()
        messages.success(request, "Regalo prenotato con successo!")

    return redirect('lista_pubblica')