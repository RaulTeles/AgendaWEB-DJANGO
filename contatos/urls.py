from django.urls import path
from . import views

urlpatterns = [
    path ('', views.index, name = 'index'),
    path ('busca/', views.busca, name = 'busca'), #Colocando <> para adicioanr as tags, e dps colocar um argumento para enviar
    path ('<int:contato_id>', views.ver_contato, name = 'ver_contato'), #Colocando <> para adicioanr as tags, e dps colocar um argumento para enviar
]