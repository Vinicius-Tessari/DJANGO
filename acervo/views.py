from django.http import HttpResponse

def home(request):
    return HttpResponse("Roteamento OK! App acervo carregado.")
