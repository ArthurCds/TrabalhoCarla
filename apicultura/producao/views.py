from audioop import reverse
from unittest import TestCase
from django.shortcuts import redirect, render
from django.test import Client
from django.urls import reverse_lazy
from django.views import View
from .forms import ColetaForm, CriacaoForm
from .models import Coleta
from django.views.generic import ListView
from django.views.generic import UpdateView
from django.views.generic import DeleteView
from django.views.generic.edit import CreateView

def criar_coleta(request):
    if request.method == 'POST':
        form = CriacaoForm(request.POST)
        if form.is_valid():
            # Processar o formulário e salvar os dados
            form.save()
            # Redirecionar para uma página de sucesso ou exibir uma mensagem de sucesso
            return render(request, 'sucesso.html')
    else:
        form = CriacaoForm()

    return render(request, 'criar_coleta.html', {'form': form})

class ListarColetasView(ListView):
    model = Coleta
    template_name = 'listar_coletas.html'  # Atualize o caminho do template aqui

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # Adicionar outros dados ao contexto, se necessário
        return context

def detalhes_coleta(request, coleta_id):
    coleta = Coleta.objects.get(pk=coleta_id)
    return render(request, 'producao/detalhes_coleta.html', {'coleta': coleta})

class DeletarColetaView(DeleteView):
    model = Coleta
    template_name = 'deletar_coleta.html'
    success_url = reverse_lazy('listar_coletas')

class ColetaCreateView(CreateView):
    model = Coleta
    form_class = ColetaForm
    template_name = 'coleta_create.html'
    success_url = '/coleta/lista/'  # ou a URL correta para a lista de coletas

    def form_valid(self, form):
        self.object = form.save()
        return redirect(self.get_success_url())

class ColetaListView(ListView):
    model = Coleta
    template_name = 'coleta_list.html'
    context_object_name = 'coletas'

class ColetaUpdateView(UpdateView):
    model = Coleta
    form_class = ColetaForm
    template_name = 'coleta_update.html'
    success_url = '/coleta/lista/'
    
class RelatorioColetaView(View):
    def get(self, request):
        # Lógica para gerar o relatório de coleta
        # Aqui você pode recuperar os dados necessários e processá-los
        # para gerar o relatório desejado

        # Exemplo de dados de coleta
        coletas = [
            {'data': '2023-07-01', 'quantidade': 5},
            {'data': '2023-07-02', 'quantidade': 8},
            {'data': '2023-07-03', 'quantidade': 12},
        ]

        context = {
            'coletas': coletas,
        }

        return render(request, 'relatorio_coleta.html', context)
    
    class RelatorioColetaViewTest(TestCase):
        def setUp(self):
            self.client = Client()

    def test_url(self):
        url = reverse('relatorio_coleta')
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)

    def test_template_used(self):
        url = reverse('relatorio_coleta')
        response = self.client.get(url)
        self.assertTemplateUsed(response, 'relatorio_coleta.html')

    def test_exibe_relatorio_corretamente(self):
        # Simulando dados de coleta
        coletas = [
            {'data': '2023-07-01', 'quantidade': 5},
            {'data': '2023-07-02', 'quantidade': 8},
            {'data': '2023-07-03', 'quantidade': 12},
        ]

        # Inserir lógica para preparar os dados de coleta (pode ser um mock de dados)

        # Simulando o contexto para renderizar o template
        context = {
            'coletas': coletas,
        }

        url = reverse('relatorio_coleta')
        response = self.client.get(url)

        # Verificar se os dados de coleta estão sendo exibidos corretamente no template
        for coleta in coletas:
            self.assertContains(response, coleta['data'])
            self.assertContains(response, str(coleta['quantidade']))

        # Verificar outros elementos do template, se necessário
        # ...