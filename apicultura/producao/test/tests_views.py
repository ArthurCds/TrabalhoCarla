from django.test import TestCase
from django.urls import reverse
from producao.models import Criacao, Coleta
from datetime import date, timedelta

class ListarColetasViewTestCase(TestCase):
    def setUp(self):
        # Criação de instâncias de Criacao
        criacao1 = Criacao.objects.create(raca='Criacao 1', data_entrada=date.today())
        criacao2 = Criacao.objects.create(raca='Criacao 2', data_entrada=date.today())
        criacao3 = Criacao.objects.create(raca='Criacao 3', data_entrada=date.today())

        # Criação de instâncias de Coleta associadas às criações
        coleta1 = Coleta.objects.create(criacao=criacao1, data=date.today(), quantidade=10)
        coleta2 = Coleta.objects.create(criacao=criacao2, data=date.today(), quantidade=5)
        coleta3 = Coleta.objects.create(criacao=criacao3, data=date.today(), quantidade=8)

def test_url_correta(self):
    url = reverse('listar_coletas')
    self.assertEqual(url, '/coletas/listar_coletas/')

    def test_usa_template_correto(self):
        response = self.client.get(reverse('listar_coletas'))
        self.assertTemplateUsed(response, 'coleta/listar_coletas.html')

    def test_lista_todas_coletas(self):
        response = self.client.get(reverse('listar_coletas'))
        coletas = Coleta.objects.all()

        for coleta in coletas:
            self.assertContains(response, coleta.criacao.raca)
            self.assertContains(response, str(coleta.data))
            self.assertContains(response, str(coleta.quantidade))

class DetalhesColetaViewTestCase(TestCase):
    def setUp(self):
        # Criação de instâncias de Criacao
        criacao1 = Criacao.objects.create(raca='Criacao 1', data_entrada=date.today())

        # Criação de instância de Coleta associada à criação
        self.coleta = Coleta.objects.create(criacao=criacao1, data=date.today(), quantidade=10)

def test_url_correta(self):
    url = reverse('detalhes_coleta', args=[self.coleta.id])
    self.assertEqual(url, f'/coletas/{self.coleta.id}/')

def test_usa_template_correto(self):
    response = self.client.get(reverse('detalhes_coleta', args=[self.coleta.id]))
    self.assertTemplateUsed(response, 'producao/detalhes_coleta.html')

def test_mostra_detalhes_corretos(self):
    response = self.client.get(reverse('detalhes_coleta', args=[self.coleta.id]))
    self.assertContains(response, self.coleta.criacao.raca)
    self.assertContains(response, str(self.coleta.data.strftime('%Y-%m-%d')))
    self.assertContains(response, str(self.coleta.quantidade))
    

class DeletarColetaViewTestCase(TestCase):
    def setUp(self):
    # Criação de uma instância de Criacao para o teste
        criacao = Criacao.objects.create(raca='Criacao de teste', data_entrada=date.today())
    # Criação de uma instância de Coleta com a instância correta de Criacao
        self.coleta = Coleta.objects.create(criacao=criacao, data=date.today(), quantidade=10)


    def test_url_correta(self):
        url = reverse('deletar_coleta', args=[self.coleta.pk])
        self.assertEqual(url, '/coletas/deletar/1/')

    def test_usa_template_correto(self):
        response = self.client.get(reverse('deletar_coleta', args=[self.coleta.pk]))
        self.assertTemplateUsed(response, 'deletar_coleta.html')

    def test_deleta_coleta(self):
        response = self.client.post(reverse('deletar_coleta', args=[self.coleta.pk]))
        self.assertEqual(response.status_code, 302)
        self.assertFalse(Coleta.objects.filter(pk=self.coleta.pk).exists())

class CriarColetaViewTestCase(TestCase):
    def test_url_correta(self):
        url = reverse('criar_coleta')
        self.assertEqual(url, '/coletas/criar_coleta/')

    def test_usa_template_correto(self):
        response = self.client.get(reverse('criar_coleta'))
        self.assertTemplateUsed(response, 'coleta/criar_coleta.html')

    def test_cria_corretamente_o_objeto(self):
        dados_coleta = {
            'criacao': 'Criacao de teste',  # Substituir pelo ID válido de uma Criacao existente
            'data': '2023-07-18',  # Data válida
            'quantidade': 15,
        }

        response = self.client.post(reverse('criar_coleta'), data=dados_coleta)

        self.assertEqual(response.status_code, 200)  # Ou 302 se houver redirecionamento
        self.assertTrue(Coleta.objects.filter(data='2023-07-18', quantidade=15).exists())
class EditarColetaViewTestCase(TestCase):
    def setUp(self):
        # Criação de uma instância de Criacao para o teste
        criacao = Criacao.objects.create(raca='Criacao de teste', data_entrada=date.today())
        # Criação de uma instância de Coleta com a instância correta de Criacao
        self.coleta = Coleta.objects.create(criacao=criacao, data=date.today(), quantidade=10)

    def test_url_correta(self):
        url = reverse('editar_coleta', args=[self.coleta.pk])
        self.assertEqual(url, f'/coletas/editar/{self.coleta.pk}/')

    def test_usa_template_correto(self):
        response = self.client.get(reverse('editar_coleta', args=[self.coleta.pk]))
        self.assertTemplateUsed(response, 'coleta/editar_coleta.html')

    def test_edita_corretamente_o_objeto(self):
        dados_editados = {
            'criacao': self.coleta.criacao.id,
            'data': date.today() + timedelta(days=2),
            'quantidade': 20,
        }

        response = self.client.post(reverse('editar_coleta', args=[self.coleta.pk]), data=dados_editados)

        self.assertEqual(response.status_code, 302)  # Redirecionamento após a edição
        self.coleta.refresh_from_db()
        self.assertEqual(self.coleta.data.strftime('%Y-%m-%d'), (date.today() + timedelta(days=2)).strftime('%Y-%m-%d'))
        self.assertEqual(self.coleta.quantidade, 20)