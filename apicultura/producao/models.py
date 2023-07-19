from django.db import models

class Criacao(models.Model):
    id = models.AutoField(primary_key=True)
    raca = models.CharField(max_length=100, verbose_name='Raça')
    data_entrada = models.DateField(verbose_name='Data de Entrada')

    def __str__(self):
        return f"ID: {self.id}, Raça: {self.raca}, Data de Entrada: {self.data_entrada}"


class Coleta(models.Model):
    id = models.AutoField(primary_key=True)
    criacao = models.ForeignKey(Criacao, on_delete=models.CASCADE, verbose_name='Criação')
    data = models.DateField(verbose_name='Data')
    quantidade = models.IntegerField(verbose_name='Quantidade')

    def __str__(self):
        return f"ID: {self.id}, Criação: {self.criacao}, Data: {self.data}, Quantidade: {self.quantidade}"
