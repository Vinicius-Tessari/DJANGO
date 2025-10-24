from django.shortcuts import render, redirect
from django.views.generic import ListView
from django.contrib import messages
from django.utils import timezone
from .models import Livro, Revista, MidiaDigital, Emprestimo
from .forms import EmprestimoForm


def home(request):
    return render(request, 'acervo/home.html')

