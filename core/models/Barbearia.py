from django.conf import settings
from django.contrib.auth.models import User
from django.db import models

# Lista de unidades federativas do Brasil (sigla, nome)
class Estados(models.TextChoices):
    AC = 'AC', 'Acre'
    AL = 'AL', 'Alagoas'
    AP = 'AP', 'Amapá'
    AM = 'AM', 'Amazonas'
    BA = 'BA', 'Bahia'
    CE = 'CE', 'Ceará'
    DF = 'DF', 'Distrito Federal'
    ES = 'ES', 'Espírito Santo'
    GO = 'GO', 'Goiás'
    MA = 'MA', 'Maranhão'
    MT = 'MT', 'Mato Grosso'
    MS = 'MS', 'Mato Grosso do Sul'
    MG = 'MG', 'Minas Gerais'
    PA = 'PA', 'Pará'
    PB = 'PB', 'Paraíba'
    PR = 'PR', 'Paraná'
    PE = 'PE', 'Pernambuco'
    PI = 'PI', 'Piauí'
    RJ = 'RJ', 'Rio de Janeiro'
    RN = 'RN', 'Rio Grande do Norte'
    RS = 'RS', 'Rio Grande do Sul'
    RO = 'RO', 'Rondônia'
    RR = 'RR', 'Roraima'
    SC = 'SC', 'Santa Catarina'
    SP = 'SP', 'São Paulo'
    SE = 'SE', 'Sergipe'
    TO = 'TO', 'Tocantins'
class Barbearia(models.Model):
    nome = models.CharField(max_length=100, blank=False, null=False)
    cnpj = models.CharField(max_length=14, blank=False, null=False, default='1')
    cep = models.CharField(max_length=20, blank=True, null=True)
    uf = models.CharField(max_length=2, choices=Estados.choices, blank=True, null=True)
    cidade = models.CharField(max_length=50, blank=True, null=True)
    endereco = models.CharField(max_length=50, blank=False, null=False)
    telefone = models.CharField(max_length=11, blank=False, null=False)
    email = models.EmailField(max_length=200, blank=False, null=False)
    descricao = models.TextField(max_length=500, blank=True, null=True) 
    comodidades = models.ManyToManyField('Comodidades', blank=True)

    def __str__(self):
        return f"{self.nome}"

class Comodidades(models.Model):
    nome = models.CharField(max_length=100, blank=False, null=False)

    def __str__(self):
        return self.nome

class servicos_oferecidos(models.Model):
    nome_do_servico = models.CharField(max_length=30, blank=False, null=False)
    valor_do_servico = models.DecimalField(max_digits=4, decimal_places=2, blank=False, null=False)
    tempo_estimado = models.DurationField(blank=False, null=False)
    descricao_do_servico = models.CharField(max_length=100, blank=True, null=True)

    def __str__(self):
        return f"{self.nome_do_servico}, {self.valor_do_servico}, {self.tempo_estimado}"

class Dias_da_semana(models.IntegerChoices):
    SEGUNDA = 1, 'segunda-feira'
    TERCA = 2, 'terça-feira'
    QUARTA = 3, 'quarta-feira'
    QUINTA = 4, 'quinta-feira'
    SEXTA = 5, 'sexta-feira'
    SABADO = 6, 'sábado'
    DOMINGO = 0, 'domingo'

class Horario_de_funcionamento(models.Model):
    barbearia = models.ForeignKey(Barbearia, on_delete=models.CASCADE, related_name="horarios")

    dia_da_semana = models.IntegerField(
        blank=False, 
        null=False, 
        choices=Dias_da_semana.choices
    )
    horario_abertura = models.TimeField(blank=False, null=False)
    horario_fechamento = models.TimeField(blank=False, null=False)

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=["barbearia", "dia_da_semana"],
                name="unique_dia_por_barbearia"
            )
        ]

    def __str__(self):
        return f"{self.barbearia.nome} - {self.get_dia_da_semana_display()}"

class Agendamento (models.Model):
    horario = models.DateTimeField(blank=False, null=False)
    horario_agendamento = models.DateTimeField(auto_now_add=True)
    cancelado = models.BooleanField(default=False)
    taxa_cancelamento = models.DecimalField(max_digits=6, decimal_places=2, null=True, blank=True)
    cliente  = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    servico = models.ForeignKey(servicos_oferecidos, on_delete=models.CASCADE)


