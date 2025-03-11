from django.db import models

class PostoTrabalho(models.Model):
    nome = models.CharField(max_length=100)
    descricao = models.TextField()
    def __str__(self):
        return self.nome
    
class Classificacao(models.Model):
    nome = models.CharField(max_length=100)
    def __str__(self):
        return self.nome

class Operacao(models.Model):
    nome = models.CharField(max_length=100)
    descricao = models.TextField()
    classificacao = models.ForeignKey(Classificacao, on_delete=models.CASCADE, )
    def __str__(self):
        return self.nome

class Maquina(models.Model):
    nome = models.CharField(max_length=100)
    descricao = models.TextField()
    operacoes = models.ManyToManyField(Operacao, related_name="maquinas")  # Nova relação
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


###################################################

class PostoTrabalho_Py(models.Model):
    nome = models.CharField(max_length=100)
    descricao = models.TextField()
    def __str__(self):
        return self.nome
    
class Classificacao_Py(models.Model):
    nome = models.CharField(max_length=100)
    def __str__(self):
        return self.nome

class Operacao_Py(models.Model):
    nome = models.CharField(max_length=100)
    descricao = models.TextField()
    classificacao = models.ForeignKey(Classificacao_Py, on_delete=models.CASCADE, )
    def __str__(self):
        return self.nome

class Maquina_Py(models.Model):
    nome = models.CharField(max_length=100)
    descricao = models.TextField()
    operacoes = models.ManyToManyField(Operacao_Py, related_name="maquinas")  # Nova relação
    def __str__(self):
        return self.nome

class Atividade_Py(models.Model):
    nome = models.CharField(max_length=255, default='Atividade Padrão')
    data_hora_inicio = models.TextField()
    data_hora_fim = models.TextField()
    observacao = models.TextField(null=True, blank=True)
    posto_trabalho = models.ForeignKey(PostoTrabalho_Py, on_delete=models.CASCADE)
    maquina = models.ForeignKey(Maquina_Py, on_delete=models.CASCADE)
    tempo_total = models.BigIntegerField(blank=True, default=0)

    def __str__(self):
        return self.nome

class Tempos_Py(models.Model):
    tempo = models.PositiveBigIntegerField(blank=True, default=0)
    atividade = models.ForeignKey(Atividade_Py, on_delete=models.CASCADE)
    operacao = models.ForeignKey(Operacao_Py, on_delete=models.CASCADE)