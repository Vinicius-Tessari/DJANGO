from django.urls import path
from . import views


urlpatterns = [
    path('', views.home, name='home'),
    path('itens/', views.ItemListView.as_view(), name='itens'),
    path('emprestimos/', views.EmprestimoListView.as_view(), name='emprestimos'),
    path('emprestar/', views.emprestimo_create, name='emprestar'),
]

