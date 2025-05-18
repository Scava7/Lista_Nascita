from django.shortcuts import render, redirect, get_object_or_404
from django.template.loader import render_to_string
from django.http import JsonResponse
from .models import Regalo, ImpostazioniPagina, UtenteRegistrato
from .forms import RegistrazioneForm, LoginForm
from django.contrib import messages
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
    regali_utente = []
    utente_id = request.session.get('utente_id')
    if utente_id:
        try:
            utente = UtenteRegistrato.objects.get(pk=utente_id)
            regali_utente = Regalo.objects.filter(prenotato_da=utente)
        except UtenteRegistrato.DoesNotExist:
            pass

    impostazioni = ImpostazioniPagina.objects.first()
    return render(request, 'lista/lista_pubblica.html', {
        'regali': regali,
        'impostazioni': impostazioni,
        'ordine_attivo': ordine,
        'utente': utente,
        'regali_utente': regali_utente  # ← AGGIUNTO QUESTO
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


def login_utente(request):
    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            try:
                utente = UtenteRegistrato.objects.get(email=form.cleaned_data['email'])
                request.session['utente_id'] = utente.id
                return redirect('lista_pubblica')
            except UtenteRegistrato.DoesNotExist:
                messages.error(request, "Email non trovata. Registrati prima.")
    else:
        form = LoginForm()

    return render(request, 'lista/login.html', {'form': form})

@require_POST
def logout_utente(request):
    request.session.flush()  # elimina tutta la sessione
    return redirect('lista_pubblica')

@require_POST
def cambia_nome(request):
    utente_id = request.session.get('utente_id')
    if not utente_id:
        return redirect('lista_pubblica')

    nuovo_nome = request.POST.get('nome', '').strip()
    if nuovo_nome:
        try:
            utente = UtenteRegistrato.objects.get(pk=utente_id)
            utente.nome = nuovo_nome
            utente.save()
        except UtenteRegistrato.DoesNotExist:
            pass

    return redirect('lista_pubblica')

@require_POST
def annulla_prenotazione(request, regalo_id):
    utente_id = request.session.get('utente_id')
    is_ajax = request.headers.get('x-requested-with') == 'XMLHttpRequest'

    regalo = get_object_or_404(Regalo, pk=regalo_id, prenotato_da_id=utente_id)

    regalo.prenotato = False
    regalo.prenotato_da = None
    regalo.save()

    if is_ajax:
        card_html = render_to_string('lista/partials/card.html', {
            'regalo': regalo,
            'request': request
        })
        return JsonResponse({'success': True, 'html': card_html})

    return redirect('lista_pubblica')

@require_POST
def prenota_regalo(request, regalo_id):
    utente_id = request.session.get('utente_id')
    is_ajax = request.headers.get('x-requested-with') == 'XMLHttpRequest'

    if not utente_id:
        if is_ajax:
            return JsonResponse({
                'success': False,
                'message': 'Devi essere registrato per prenotare.'
            })
        return redirect('registrazione')

    regalo = get_object_or_404(Regalo, pk=regalo_id)

    if not regalo.prenotato:
        regalo.prenotato = True
        regalo.prenotato_da_id = utente_id
        regalo.save()

    if is_ajax:
        card_html = render_to_string('lista/partials/card.html', {
            'regalo': regalo,
            'request': request
        })
        minicard_html = render_to_string('lista/partials/minicard.html', {
            'r': regalo,
            'request': request
        })
        return JsonResponse({
            'success': True,
            'html': card_html,
            'minicard': minicard_html
        })

    return redirect('lista_pubblica')