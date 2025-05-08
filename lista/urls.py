from django.urls import path
from . import views

urlpatterns = [
    path('', views.lista_pubblica, name='lista_pubblica'),
]