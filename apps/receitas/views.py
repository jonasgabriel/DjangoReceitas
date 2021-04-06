from django.shortcuts import render, redirect, get_object_or_404
from setuptools.namespaces import flatten
from django.contrib.auth.models import User
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from .models import Receita


def index(request):
    if Receita.objects.filter(publicar=True).exists():
        receitas = Receita.objects.filter(publicar=True)
        paginator = Paginator(receitas, 3)
        page = request.GET.get('page')
        page_obj = paginator.get_page(page)

        receitas_dict = {'page_obj': page_obj}
        return render(request, 'in', receitas_dict)
    return render(request, 'index.html')


def receita(request, receita_id):
    receitas = get_object_or_404(Receita, pk=receita_id)
    receitas = {'receitas': receitas,
                'categorias': Receita.objects.values('categoria').distinct('categoria')
                }
    return render(request, 'receita.html', receitas)


def buscar_receita(request):
    lista_receitas = Receita.objects.filter(publicar=True)
    if 'search' in request.GET:
        nome_a_buscar = request.GET['search']
        if nome_a_buscar:
            lista_receitas = lista_receitas.filter(nome_receita__icontains=nome_a_buscar)

    dados = {'receitas': lista_receitas}
    return render(request, 'buscar.html', dados)


def cria_receita(request):
    if request.user.is_authenticated:
        if request.method == 'POST':
            dados = {
                'nome_receita': request.POST['nome_receita'].strip(),
                'ingredientes': request.POST['ingredientes'].strip(),
                'modo_preparo': request.POST['modo_preparo'].strip(),
                'tempo_preparo': request.POST['tempo_preparo'].strip(),
                'rendimento': request.POST['rendimento'].strip(),
                'categoria': request.POST['categoria'].strip(),
                'foto': request.FILES['foto_receita']
            }
            pessoa = get_object_or_404(User, pk=request.user.id)
            if not Receita.objects.filter(nome_receita=dados['nome_receita']).exists():
                receita = Receita.objects.create(pessoa=pessoa, **dados)
                receita.save()
            return redirect('dashboard')
        return render(request, 'usuarios/cria_receita.html')
    return redirect('index')


def deletar_receita(request, receita_id):
    if request.user.is_authenticated:
        receita = get_object_or_404(Receita, pk=receita_id)
        receita.delete()
        return redirect('dashboard')
    return redirect('index')


def editar_receita(request, receita_id):
    if request.user.is_authenticated:
        receita = get_object_or_404(Receita, pk=receita_id)
        receita_a_editar = {'receita': receita}
        return render(request, 'usuarios/edita_receita.html', receita_a_editar)
    return redirect('index')


def atualiza_receita(request):
    if request.user.is_authenticated:
        if request.method == 'POST':
            receita = Receita.objects.get(pk=request.POST['id'])
            receita.nome_receita = request.POST['nome_receita'].strip()
            receita.ingredientes = request.POST['ingredientes'].strip()
            receita.modo_preparo = request.POST['modo_preparo'].strip()
            receita.tempo_preparo = request.POST['tempo_preparo'].strip()
            receita.rendimento = request.POST['rendimento'].strip()
            receita.categoria = request.POST['categoria'].strip()
            if 'foto_receita' in request.FILES:
                receita.foto = request.FILES['foto_receita']
            receita.save()
        return redirect('dashboard')
    return render(request, 'index.html')
