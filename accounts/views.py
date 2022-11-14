from email import message
from importlib.metadata import requires
from urllib.parse import uses_relative
from django.shortcuts import render
#importando um redirecionador para quando cadastrar jogar para outra pagina
from django.shortcuts import redirect
from django.contrib import messages
#importando classe para chegar se o login e senha está válido
from django.contrib import auth
#importando validador de emails
from django.core.validators import validate_email
#importando veriaficador para que não possuam usuários/emais ja cadastrados
from django.contrib.auth.models import User
#importando modulo para limitar pagina apenas para usuario logado
from django.contrib.auth.decorators import login_required
from .models import FormContato



def login(request):
    #Se nada for postado exibe a pagina de cadastro
    if request.method != 'POST':
        return render(request, 'accounts/login.html')
    

    usuario = request.POST.get('usuario')
    senha = request.POST.get('senha')

    #checando se o usuario e seha existe
    user = auth.authenticate(request, username = usuario, password = senha)
    if not user:
        messages.error(request, 'Usuário ou senha incorreto')
        return render(request, 'accounts/login.html')
    else:
        auth.login(request, user)
        messages.error(request, 'Você fez o Login com sucesso')
        return redirect ('inicio')

   

@login_required(redirect_field_name='index_login')
def inicio(request):
    if request.method != 'POST':    
        return render(request, 'accounts/inicio.html')
    

def index_login(request):
    auth.logout(request)
    return redirect ('login')


@login_required(redirect_field_name='/')
def logout(request):
    auth.logout(request)
    return render(request, '/accounts/login')




def cadastro(request):
    #Se nada for postado exibe a pagina de cadastro
    if request.method != 'POST':    
        return render(request, 'accounts/cadastro.html')

    #CRIANDO VARIAVEIS PARA A PAGINA
    email = request.POST.get('email')
    nome = request.POST.get('nome')
    sobrenome = request.POST.get('sobrenome')
    usuario = request.POST.get('usuario')
    senha = request.POST.get('senha')
    senha2 = request.POST.get('senha2')

    #checando para nenhum nome ser vazio
    if not nome or not sobrenome or not email or not usuario or not senha or not senha2:
        messages.error(request, 'Nenhum campo pode ficar vazio.')
        return render(request, 'accounts/cadastro.html')

    #validando o email
    try:
        validate_email(email)
    except:
        messages.error(request, 'Email Inválido.')
        return render(request, 'accounts/cadastro.html')
    
    #Regrando que o usuário tenha que ser mais de 6 caracteres
    if len(usuario)< 6:
        messages.error(request, 'O Usuário precisa ter mais de 6 Caracteres')
        return render(request, 'accounts/cadastro.html')
    
    #Regrando que a senha tenha que ser mais de 6 caracteres
    if len(senha)< 6:
        messages.error(request, 'A senha precisa ter mais de 6 Caracteres')
        return render(request, 'accounts/cadastro.html')        
    
    #Chegando se as senhas são iguais
    if senha != senha2:
        messages.error(request, 'As senhas não são iguais.')
        return render(request, 'accounts/cadastro.html')       
   
    #Checando se o usuário ja existe
    if User.objects.filter(username = usuario).exists():
        messages.error(request, 'O Usuário ja existe.')
        return render(request, 'accounts/cadastro.html')  

    #Checando se o usuário ja existe
    if User.objects.filter(username = email).exists():
        messages.error(request, 'Este email ja existe.')
        return render(request, 'accounts/cadastro.html')   

    messages.success(request, 'Usuário Cadastrado com Sucesso! Agora você pode fazer o login.')

    #criando o usuario para fazer login
    user = User.objects.create_user(username = usuario, email = email, password= senha, first_name = nome, last_name = sobrenome)
    user.save()
    #Redirecionando para outra pagina após o cadastro
    return redirect('login')
    

#caso alguem tente acessar essa pagina, e nao estiver logado, va ser jogado para o /login
@login_required(redirect_field_name='index_login')
def dashboard(request):

    if request.method != 'POST':
        form = FormContato()
        return render(request, 'accounts/dashboard.html',{'form': form})

    form = FormContato(request.POST, request.FILES)
    if not form.is_valid():
        messages.error(request, 'Erro ao enviar formulário')
        form = FormContato()
        return render(request, 'accounts/dashboard.html',{'form': form})

    form.save()
    messages.success(request, f'Contato {request.POST.get("nome")} salvo com sucesso')
    return redirect ('dashboard')
# Create your views here.
