from django.urls import path
from . import views

urlpatterns = [
    path('registrazione/', views.registrazione_utente, name='registrazione'),
    path('', views.lista_pubblica, name='lista_pubblica'),
    path('prenota/<int:regalo_id>/', views.prenota_regalo, name='prenota_regalo'),
    path('utente/', views.pagina_utente, name='pagina_utente'),
    path('logout/', views.logout_utente, name='logout_utente'),
]