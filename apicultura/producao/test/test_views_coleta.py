from datetime import date
from django.shortcuts import redirect, render
from django.test import TestCase, Client
from django.urls import reverse
from django.views import View
from producao.models import Coleta
from producao.forms import ColetaForm


class ColetaCreateView(View):
    def get(self, request):
        form = ColetaForm()
        return render(request, 'coleta_create.html', {'form': form})

    def post(self, request):
        form = ColetaForm(request.POST)
        if form.is_valid():
            form.save(commit=False)
            coleta = Coleta.objects.create(
                data=form.cleaned_data['data'],
                quantidade=form.cleaned_data['quantidade'],
                criacao=None
            )
            assert coleta is not None, "A coleta não foi criada corretamente"
            assert coleta.data == form.cleaned_data['data'], "A data da coleta não corresponde ao valor fornecido"
            assert coleta.quantidade == form.cleaned_data['quantidade'], "A quantidade da coleta não corresponde ao valor fornecido"
            return redirect('coleta_lista')  # Certifique-se de que 'coleta_lista' seja a URL correta para a lista de coletas
        return render(request, 'coleta_create.html', {'form': form})


class ColetaCreateViewTest(TestCase):
    def setUp(self):
        self.client = Client()

    def test_url(self):
        url = reverse('coleta_create')
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'coleta_create.html')

    def test_template(self):
        url = reverse('coleta_create')
        response = self.client.get(url)
        self.assertTemplateUsed(response, 'coleta_create.html')

    def test_create_coleta(self):
        url = reverse('coleta_create')
        data = {
            'data': '2023-07-05',
            'quantidade': 10
        }
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, 302)

        coleta = Coleta.objects.last()
        self.assertIsNotNone(coleta)
        self.assertEqual(coleta.data, date(2023, 7, 5))
        self.assertEqual(coleta.quantidade, 10)


class ColetaListViewTest(TestCase):
    def setUp(self):
        self.client = Client()

    def test_url(self):
        url = reverse('coleta_lista')
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'coleta_lista.html')

    def test_template(self):
        url = reverse('coleta_lista')
        response = self.client.get(url)
        self.assertTemplateUsed(response, 'coleta_lista.html')

    def test_list_coletas(self):
        # Cria algumas coletas para testar a listagem
        coleta1 = Coleta.objects.create(data=date.today(), quantidade=5, criacao=None)
        coleta2 = Coleta.objects.create(data=date.today(), quantidade=8, criacao=None)

        url = reverse('coleta_lista')
        response = self.client.get(url)

        # Verifica se a resposta contém as coletas criadas
        self.assertContains(response, coleta1.data)
        self.assertContains(response, coleta1.quantidade)
        self.assertContains(response, coleta2.data)
        self.assertContains(response, coleta2.quantidade)

        # Verifica se o template usado é o correto
        self.assertTemplateUsed(response, 'coleta_lista.html')


class ColetaDetailViewTest(TestCase):
    def setUp(self):
        self.client = Client()
        self.coleta = Coleta.objects.create(data=date.today(), quantidade=10, criacao=None)

    def test_url(self):
        url = reverse('coleta_detalhes', args=[self.coleta.pk])
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'coleta_detalhes.html')

    def test_template(self):
        url = reverse('coleta_detalhes', args=[self.coleta.pk])
        response = self.client.get(url)
        self.assertTemplateUsed(response, 'coleta_detalhes.html')

    def test_show_coleta_details(self):
        url = reverse('coleta_detalhes', args=[self.coleta.pk])
        response = self.client.get(url)

        # Verifica se a resposta contém os detalhes corretos da coleta
        self.assertContains(response, self.coleta.data)
        self.assertContains(response, self.coleta.quantidade)

        # Verifica se o template usado é o correto
        self.assertTemplateUsed(response, 'coleta_detalhes.html')


class ColetaDeleteViewTest(TestCase):
    def setUp(self):
        self.client = Client()
        self.coleta = Coleta.objects.create(data=date.today(), quantidade=10, criacao=None)

    def test_url(self):
        url = reverse('coleta_deletar', args=[self.coleta.pk])
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'coleta_deletar.html')

    def test_template(self):
        url = reverse('coleta_deletar', args=[self.coleta.pk])
        response = self.client.get(url)
        self.assertTemplateUsed(response, 'coleta_deletar.html')

    def test_delete_coleta(self):
        url = reverse('coleta_deletar', args=[self.coleta.pk])
        response = self.client.post(url)
        self.assertRedirects(response, reverse('coleta_lista'))
        self.assertFalse(Coleta.objects.filter(pk=self.coleta.pk).exists())
