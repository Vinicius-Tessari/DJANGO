from django.contrib import admin
from .models import Livro, Revista, MidiaDigital, Emprestimo


@admin.register(Livro)
class LivroAdmin(admin.ModelAdmin):
    list_display = ('codigo', 'titulo', 'autor', 'estoque')
    search_fields = ('codigo', 'titulo', 'autor', 'isbn')

@admin.register(Revista)
class RevistaAdmin(admin.ModelAdmin):
    list_display = ('codigo', 'titulo', 'edicao', 'estoque')
    search_fields = ('codigo', 'titulo', 'edicao')

@admin.register(MidiaDigital)
class MidiaDigitalAdmin(admin.ModelAdmin):
    list_display = ('codigo', 'titulo', 'ano')
    search_fields = ('codigo', 'titulo')
    
@admin.register(Emprestimo)
class EmprestimoAdmin(admin.ModelAdmin):
    list_display = ('item', 'usuario', 'criado_em', 'devolvido_em')
    list_filter = ('criado_em', 'devolvido_em')
    search_fields = ('usuario__username',)
