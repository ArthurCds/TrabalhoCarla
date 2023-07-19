from django.contrib import admin
from django.urls import path
from producao.views import criar_coleta, ListarColetasView
from producao.views import detalhes_coleta, DeletarColetaView
from producao.views import ColetaCreateView
from producao.views import ColetaListView, ColetaUpdateView, RelatorioColetaView



urlpatterns = [
    path('admin/', admin.site.urls),
    path('coleta/criar/', criar_coleta, name='criar_coleta'),
    path('listar_coletas/', ListarColetasView.as_view(), name='listar_coletas'),
    path('coletas/<int:coleta_id>/', detalhes_coleta, name='detalhes_coleta'),
    path('coletas/deletar/<int:pk>/', DeletarColetaView.as_view(), name='deletar_coleta'),
    path('coleta/create/', ColetaCreateView.as_view(), name='coleta_create'),
    path('coleta/lista/', ColetaListView.as_view(), name='coleta_list'),
    path('coleta/update/<int:pk>/', ColetaUpdateView.as_view(), name='coleta_update'),
    path('coleta/relatorio/', RelatorioColetaView.as_view(), name='relatorio_coleta'),
    path('coleta/create/', ColetaCreateView.as_view(), name='coleta_create'),
    path('relatorio/coleta/', RelatorioColetaView.as_view(), name='relatorio_coleta'),
]
