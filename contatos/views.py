from django.shortcuts import render, get_object_or_404, redirect
from .models import Contato
from django.core.paginator import Paginator
from django.http import Http404
from django.db.models import Q, Value
from django.db.models.functions import Concat
from django.contrib import messages
from django.contrib.auth.decorators import login_required


@login_required(redirect_field_name='index_login')
def index(request):

    # contato = Contato.objects.all() #criando uma variavel e adicionando o objetct all da classe Contato
    contato = Contato.objects.order_by('id') #criando uam variavel e adicionando elas de formas decrescentes

    paginator = Paginator(contato,5)
    page = request.GET.get('page')
    contato = paginator.get_page(page)

    return render(request, 'contatos/index.html',{
        'contatos': contato #Criando uma chave para o arquivo index.html para fazer um for e os valores ficarem dinamicos
    })
@login_required(redirect_field_name='index_login')
def ver_contato(request,contato_id):
    # try:
    contato = get_object_or_404(Contato,id=contato_id)

    if not contato.mostrar:
        raise Http404

    return render(request, 'contatos/info_contato.html', {
        'contato': contato
    })
    # except Contato.DoesNotExist as e:
    #     raise Http404() #adicionando erro 404

@login_required(redirect_field_name='index_login')
def busca(request):
    termo = request.GET.get('termo')
    campos = Concat('nome', Value(' '), 'sobrenome') #Concatenando os campos nomes e sobrenome
  
    if termo is None or not termo:
        messages.add_message(
            request,
            messages.ERROR,
            'Você nao digitou nenhum nome, Por favor, tente novamente.'
        )
        return redirect('index')

    contato = Contato.objects.annotate( # 
        nome_completo = campos#
    ).filter(#
        Q(nome_completo__icontains = termo) | Q(telefone__icontains = termo)
    )

    '''
    contato = Contato.objects.order_by('-id').filter( #criando uam variavel e adicionando elas de formas decrescentes
        Q(nome__icontains= termo) | Q(sobrenome__icontains = termo), # importando classe Q para buscar nos campos separadamento 'OR'
    ) 
    '''
    paginator = Paginator(contato,3) # criando uma variavel para a classe Paginator, e definindo quantos contatos devem aparecer
    page = request.GET.get('page')
    contato = paginator.get_page(page)

    return render(request, 'contatos/busca.html',{
        'contatos': contato #Criando uma chave para o arquivo index.html para fazer um for e os valores ficarem dinamicos
    })
