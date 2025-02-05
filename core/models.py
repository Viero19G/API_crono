from django.db import models

class PostoTrabalho(models.Model):
    nome = models.CharField(max_length=100)
    descricao = models.TextField()
    def __str__(self):
        return self.nome

class Maquina(models.Model):
    nome = models.CharField(max_length=100)
    descricao = models.TextField()
    def __str__(self):
        return self.nome

class Operacao(models.Model):
    nome = models.CharField(max_length=100)
    descricao = models.TextField()
    classificacao = models.CharField(max_length=50)
    def __str__(self):
        return self.nome

class Atividade(models.Model):
    nome = models.CharField(max_length=255, default='Atividade Padrão')
    data_hora_inicio = models.TextField()
    data_hora_fim = models.TextField()
    observacao = models.TextField(null=True, blank=True)
    posto_trabalho = models.ForeignKey(PostoTrabalho, on_delete=models.CASCADE)
    maquina = models.ForeignKey(Maquina, on_delete=models.CASCADE)
    tempo_total = models.BigIntegerField(blank=True, default=0)

    def __str__(self):
        return self.nome

class Tempos(models.Model):
    tempo = models.PositiveBigIntegerField(blank=True, default=0)
    atividade = models.ForeignKey(Atividade, on_delete=models.CASCADE)
    operacao = models.ForeignKey(Operacao, on_delete=models.CASCADE)