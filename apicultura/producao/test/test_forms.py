from datetime import date, timedelta
from django.urls import reverse
from django.test import TestCase
from producao.forms import CriacaoForm
from producao.models import Coleta, Criacao


class CriacaoFormTest(TestCase):

    def test_form_valid(self):
        criacao = Criacao.objects.create(
            raca='Criacao 1', data_entrada=date.today())
        form_data = {
            'criacao': criacao.id,
            'raca': criacao.raca,
            'data': date.today(),
            'quantidade': 10
        }
        form = CriacaoForm(data=form_data)
        self.assertTrue(form.is_valid())

    def test_form_invalid_same_day(self):
        criacao = Criacao.objects.create(
            raca='Criacao 1', data_entrada=date.today())
        coleta = Coleta.objects.create(
            criacao=criacao, data=date.today(), quantidade=5)
        form_data = {
            'criacao': criacao.id,
            'data': date.today(),
            'quantidade': 8
        }
        form = CriacaoForm(data=form_data)
        self.assertFalse(form.is_valid())
        self.assertIn('raca', form.errors)
        self.assertIn('data_entrada', form.errors)

    def test_form_invalid_future_date(self):
        criacao = Criacao.objects.create(
            raca='Criacao 1', data_entrada=date.today())
        form_data = {
            'criacao': criacao.id,
            'data': date.today()+timedelta(days=2),
            'quantidade': 10
        }
        form = CriacaoForm(data=form_data)
        self.assertFalse(form.is_valid())
        self.assertIn('raca', form.errors)
        self.assertIn('data_entrada', form.errors)

class EdicaoColetaFormTest(TestCase):

    def setUp(self):
        self.criacao = Criacao.objects.create(
            raca='Criacao 1', data_entrada=date.today())
        self.coleta = Coleta.objects.create(
            criacao=self.criacao, data=date.today(), quantidade=5)

    def test_form_valid(self):
        form_data = {
            'criacao': self.criacao.id,
            'data': date.today(),
            'quantidade': 8
        }
        form = CriacaoForm(data=form_data, instance=self.coleta)
        self.assertTrue(form.is_valid())

    def test_form_invalid_same_day(self):
        coleta2 = Coleta.objects.create(
            criacao=self.criacao, data=date.today()+timedelta(days=1), quantidade=5)
        form_data = {
            'criacao': self.criacao.id,
            'data': coleta2.data,
            'quantidade': 8
        }
        form = CriacaoForm(data=form_data, instance=self.coleta)
        self.assertFalse(form.is_valid())
        self.assertIn('data_entrada', form.errors)

    def test_form_invalid_future_date(self):
        form_data = {
            'criacao': self.criacao.id,
            'data': date.today()+timedelta(days=2),
            'quantidade': 8
        }
        form = CriacaoForm(data=form_data, instance=self.coleta)
        self.assertFalse(form.is_valid())
        self.assertIn('data_entrada', form.errors)
