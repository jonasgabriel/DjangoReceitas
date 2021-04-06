from django.contrib import admin
from .models import Pessoas
# Register your models here.


class ListandoPessoas(admin.ModelAdmin):
    list_display = ('id', 'nome', 'email')
    list_display_links = ('id', 'nome')


admin.site.register(Pessoas, ListandoPessoas)
