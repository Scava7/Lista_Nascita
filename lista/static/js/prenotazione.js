function getCookie(name) {
    let cookieValue = null;
    if (document.cookie && document.cookie !== '') {
        const cookies = document.cookie.split(';');
        for (let cookie of cookies) {
            cookie = cookie.trim();
            if (cookie.startsWith(name + '=')) {
                cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                break;
            }
        }
    }
    return cookieValue;
}

function prenota(event, regaloId) {
    event.preventDefault();

    const form = document.getElementById(`form-${regaloId}`);
    const url = form.action;

    fetch(url, {
        method: 'POST',
        headers: {
            'X-CSRFToken': getCookie('csrftoken'),
            'X-Requested-With': 'XMLHttpRequest'
        },
    })
    .then(response => response.json())
    .then(data => {
        if (data.success && data.html) {
            const card = document.getElementById(`card-${regaloId}`);
            if (card) {
                card.outerHTML = data.html;
            }

            // Se esiste il menu laterale e la lista regali, aggiorniamo anche lì
            if (data.minicard) {
                const lista = document.querySelector('#sideMenu ul');
                if (lista) {
                    // evita doppioni
                    const esiste = document.getElementById(`mini-card-${regaloId}`);
                    if (!esiste) {
                        lista.insertAdjacentHTML('beforeend', data.minicard);
                    }
                }
            }
        }
    })
    .catch(error => {
        console.error('Errore:', error);
    });
}


function annullaPrenotazione(event, regaloId) {
    event.preventDefault();

    const form = event.target;
    const url = form.action;

    fetch(url, {
        method: 'POST',
        headers: {
            'X-CSRFToken': getCookie('csrftoken'),
            'X-Requested-With': 'XMLHttpRequest'
        },
    })
    .then(response => response.json())
    .then(data => {
        if (data.success) {
            // Rimuovi la minicard
            const miniCard = document.getElementById(`mini-card-${regaloId}`);
            if (miniCard) {
                miniCard.remove();
            }

            // Aggiorna la card principale
            if (data.html) {
                const card = document.getElementById(`card-${regaloId}`);
                if (card) {
                    card.outerHTML = data.html;
                }
            }
        } else {
            alert(data.message || 'Errore durante l’annullamento.');
        }
    })
    .catch(error => {
        console.error('Errore:', error);
    });
}

