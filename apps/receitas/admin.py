from django.contrib import admin
from .models import Receita


class ListandoReceitas(admin.ModelAdmin):
    list_display = ('id', 'nome_receita', 'foto', 'publicar',)
    list_display_links = ('id', 'nome_receita',)
    list_editable = ('publicar',)
    ordering = ['id']


# Register your models here.
admin.site.register(Receita, ListandoReceitas)

