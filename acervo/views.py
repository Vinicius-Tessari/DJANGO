from django.shortcuts import render, redirect
from django.views.generic import ListView
from django.contrib import messages
from django.utils import timezone
from .models import Livro, Revista, MidiaDigital, Emprestimo
from .forms import EmprestimoForm


def home(request):
    return render(request, 'acervo/home.html')

class ItemListView(ListView):
    template_name = 'acervo/item_list.html'
    context_object_name = 'itens'

    def get_queryset(self):
        return list(Livro.objects.all()) + list(Revista.objects.all()) + list(MidiaDigital.objects.all())
    
class EmprestimoListView(ListView):
    model = Emprestimo
    template_name = 'acervo/emprestimo_list.html'
    context_object_name = 'emprestimos'

def emprestimo_create(request):
    if request.method == 'POST':
        form = EmprestimoForm(request.POST)
        if form.is_valid():
            emp = form.save
            messages.sucess(request, f'Empréstimo criado: {emp}')
            return redirect ('emprestimos')
    else:
        form = EmprestimoForm()
    return render(request, 'acervo/emprestimo_form.html', {'form': form})

