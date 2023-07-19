from datetime import date
from django import forms
from .models import Criacao, Coleta
from django.utils import timezone

class CriacaoForm(forms.ModelForm):
    class Meta:
        model = Criacao
        fields = '__all__'

    def clean_raca(self):
        raca = self.cleaned_data['raca']
        if len(raca) > 100:
            raise forms.ValidationError("O tamanho máximo permitido para a raça é de 100 caracteres.")
        return raca
    
    def clean_data(self):
        data = self.cleaned_data['data']

        if data <= timezone.now().date():
            raise forms.ValidationError("A data da coleta não pode ser uma data passada.")


        return data
 
    def clean(self):
        cleaned_data = super().clean()
        data = cleaned_data.get('data')

        if data:
            coletas_no_mesmo_dia = Coleta.objects.filter(data=data).exists()
            if coletas_no_mesmo_dia:
                raise forms.ValidationError("Já existe uma coleta registrada para essa data.")

        return cleaned_data





class ColetaForm(forms.ModelForm):
    class Meta:
        model = Coleta
        fields = '__all__'
        
class ListarColetasForm(forms.Form):
    data_inicio = forms.DateField(label='Data de Início')
    data_fim = forms.DateField(label='Data de Fim')
    