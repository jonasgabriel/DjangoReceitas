from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('receitas/<int:receita_id>', views.receita, name='receita'),
    path('buscar', views.buscar_receita, name='buscar'),
    path('criar/receita', views.cria_receita, name='cria_receita'),
    path('deletar/<int:receita_id>', views.deletar_receita, name='deletar_receita'),
    path('editar/<int:receita_id>', views.editar_receita, name='editar_receita'),
    path('atualiza/receita', views.atualiza_receita, name='atualiza_receita'),
]

