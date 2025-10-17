from django.contrib import admin
from .models import Livro, Revista, MidiaDigital, Emprestimo

@admin.register(Livro)
class LivroAdmin(admin.ModelAdmin):
    list_display = ('codigo', 'titulo', 'autor', 'estoque')

@admin.register(Revista)
class RevistaAdmin(admin.ModelAdmin):
    list_display = ('codigo', 'titulo', 'edicao', 'estoque')

@admin.register(MidiaDigital)
class MidiaDigitalAdmin(admin.ModelAdmin):
    list_display = ('codigo', 'titulo', 'ano')

@admin.register(Emprestimo)
class EmprestimoAdmin(admin.ModelAdmin):
    list_display = ('item', 'usuario', 'criado_em', 'devolvido_em')

