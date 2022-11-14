from django.contrib import admin
from .models import Categoria, Contato
# Register your models here.

class ContatoAdmin(admin.ModelAdmin):
    list_display = ['id','nome','sobrenome','telefone','email','data_criacao','mostrar'] #Mostra os campos das listas

    list_display_links = ['id','nome','sobrenome'] #Deixa os campos 'clicavéis na pag admin'
    # list_filter = ['nome', 'sobrenome'] #cria um campo para filtrar pelos campos
    list_per_page = 10 #limita o numero de contatos mostrado na pagina
    search_fields = ['nome','sobrenome','telefone'] #Mostra o campo de pesquisa
    list_editable = ('telefone','mostrar')

admin.site.register(Categoria)
admin.site.register(Contato, ContatoAdmin)