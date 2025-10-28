from django.db import models

class Barbearia(models.Model):
    nome_da_barbearia = models.CharField(max_length=100, blank=False, null=False)
    CNPJ_da_barbearia = models.CharField(max_length=14, blank=False, null=False, default='1')
    CEP = models.CharField(max_length=10, blank=False, null=False)
    UF_da_barbearia = models.CharField(max_length=20, blank=False, null=False)
    cidade_da_barbearia = models.CharField(max_length=50, blank=False, null=False)
    endereco_da_barbearia = models.CharField(max_length=50, blank=False, null=False)
    telefone_da_barbearia = models.CharField(max_length=11, blank=False, null=False)
    email_da_barbearia = models.EmailField(max_length=200, blank=False, null=False)
    descricao_sobre_barbearia = models.TextField(max_length=500, blank=True, null=True)


class Comodidades(models.Model):
    tipo_comodidade = models.CharField(max_length=30)

    def __str__(self):
        return self.tipo_comodidade


class servicos_oferecidos(models.Model):
    nome_do_servico = models.CharField(max_length=30, blank=False, null=False)
    valor_do_servico = models.DecimalField(max_digits=4, decimal_places=2, blank=False, null=False)
    tempo_estimado = models.DurationField(blank=False, null=False)
    descricao_do_servico = models.CharField(max_length=100, blank=True, null=True)

class Dias_da_semana(models.IntegerChoices):
    SEGUNDA = 1, 'segunda-feira'
    TERCA = 2, 'terça-feira'
    QUARTA = 3, 'quarta-feira'
    QUINTA = 4, 'quinta-feira'
    SEXTA = 5, 'sexta-feira'
    SABADO = 6, 'sábado'
    DOMINGO = 0, 'domingo'

class Horario_de_funcionamento(models.Model):
    dia_da_semana = models.IntegerField(blank=False, null=False, choices=Dias_da_semana.choices)
    horario_abertura = models.TimeField(blank=False, null=False)
    horario_fechamento = models.TimeField(blank=False, null=False)    


