from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from receitas.models import Receita
from django.contrib import messages

# Create your views here.


def cadastro(request):
    if request.method == 'POST':
        nome = request.POST['nome'].strip()
        email = request.POST['email'].strip()
        password = request.POST['password'].strip()
        password2 = request.POST['password2'].strip()

        if password == password2:
            if nome and password:
                if not User.objects.filter(email=email).exists():
                    user = User.objects.create_user(username=nome, email=email, password=password)
                    user.save()
                    messages.add_message(request, messages.SUCCESS, 'Úsuario cadastrado com sucesso, faça o login')
                else:
                    messages.add_message(request, messages.ERROR, 'E-mail já cadastrado.')
        else:
            messages.add_message(request, messages.ERROR, 'Digite a mesma senha em ambos os campos de senha.')

    return render(request, 'usuarios/cadastro.html')


def login_view(request):
    if not request.user.is_authenticated:
        if request.method == 'POST':
            email = request.POST['email'].strip()
            password = request.POST['password'].strip()

            if email != '' and password != '':
                if User.objects.filter(email=email).exists():
                    username = User.objects.get(email__iexact=email).username
                    user = authenticate(request, username=username, password=password)
                    if user is not None:
                        login(request, user)
                        return redirect('dashboard')
        return render(request, 'usuarios/login.html')

    return redirect('dashboard')


def dashboard(request):
    if request.user.is_authenticated:
        receitas = Receita.objects.order_by('-data_receita').filter(pessoa__id=request.user.id)
        dados = {
            'receitas': receitas
        }
        return render(request, 'usuarios/dashboard.html', dados)
    return redirect('index')


def logout_view(request):
    if request.user.is_authenticated:
        logout(request)
    return redirect('index')

