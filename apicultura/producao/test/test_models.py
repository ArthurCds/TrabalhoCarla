from datetime import date, timedelta

from django.test import TestCase
from producao.forms import CriacaoForm
from producao.models import Coleta, Criacao


class CriacaoTestCase(TestCase):
    def test_tamanho_maximo_raca(self):
        # Criação de uma instância de Criacao com uma raça que excede o tamanho máximo permitido (100)
        criacao = Criacao(raca='Cachorro' * 100)

        # Verifica se a validação do tamanho máximo da raça é aplicada corretamente
        self.assertRaises(Exception, criacao.full_clean)


class CriacaoFormTestCase(TestCase):
    def test_elementos_obrigatorios(self):
        form = CriacaoForm(data={})  # Cria uma instância vazia do formulário

        # Verifica se o formulário é inválido quando os campos obrigatórios estão vazios
        self.assertFalse(form.is_valid())
        # Verifica se o campo 'raca' está nos erros do formulário
        self.assertIn('raca', form.errors)
        # Verifica se o campo 'data_entrada' está nos erros do formulário
        self.assertIn('data_entrada', form.errors)


class VerboseNameTestCase(TestCase):
    def test_verbose_name_criacao(self):
        # Verifica se o verbose_name do campo raca em Criacao está correto
        field = Criacao._meta.get_field('raca')
        self.assertEqual(field.verbose_name, 'Raça')

        # Verifica se o verbose_name do campo data_entrada em Criacao está correto
        field = Criacao._meta.get_field('data_entrada')
        self.assertEqual(field.verbose_name, 'Data de Entrada')

    def test_verbose_name_coleta(self):
        # Verifica se o verbose_name do campo criacao em Coleta está correto
        field = Coleta._meta.get_field('criacao')
        self.assertEqual(field.verbose_name, 'Criação')

        # Verifica se o verbose_name do campo data em Coleta está correto
        field = Coleta._meta.get_field('data')
        self.assertEqual(field.verbose_name, 'Data')

        # Verifica se o verbose_name do campo quantidade em Coleta está correto
        field = Coleta._meta.get_field('quantidade')
        self.assertEqual(field.verbose_name, 'Quantidade')


class ColetaOrdenacaoTestCase(TestCase):
    def setUp(self):
        # Criação de instâncias de Criacao
        criacao1 = Criacao.objects.create(
            raca='Cachorro', data_entrada=date.today())
        criacao2 = Criacao.objects.create(
            raca='Gato', data_entrada=date.today() - timedelta(days=1))
        criacao3 = Criacao.objects.create(
            raca='Pássaro', data_entrada=date.today() - timedelta(days=2))

        # Criação de instâncias de Coleta associadas às criações
        coleta1 = Coleta.objects.create(
            criacao=criacao1, data=date.today() - timedelta(days=2), quantidade=10)
        coleta2 = Coleta.objects.create(
            criacao=criacao2, data=date.today(), quantidade=5)
        coleta3 = Coleta.objects.create(
            criacao=criacao3, data=date.today() - timedelta(days=1), quantidade=8)

class ColetaOrdenacaoTestCase(TestCase):
    def setUp(self):
        # Criação de instâncias de Criacao
        criacao1 = Criacao.objects.create(raca='Criacao 1', data_entrada=date.today())
        criacao2 = Criacao.objects.create(raca='Criacao 2', data_entrada=date.today())
        criacao3 = Criacao.objects.create(raca='Criacao 3', data_entrada=date.today())

        # Criação de instâncias de Coleta associadas às criações
        coleta1 = Coleta.objects.create(criacao=criacao1, data=date.today(), quantidade=10)
        coleta2 = Coleta.objects.create(criacao=criacao2, data=date.today(), quantidade=5)
        coleta3 = Coleta.objects.create(criacao=criacao3, data=date.today(), quantidade=8)

    def test_coleta_ordenacao(self):
        # Verifica se as coletas estão ordenadas corretamente da mais recente para a mais antiga
        coletas = list(Coleta.objects.all().order_by('-data'))
        coletas_ordenadas = [coleta3, coleta2, coleta1]
        self.assertEqual(coletas, coletas_ordenadas)