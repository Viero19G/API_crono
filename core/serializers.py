from rest_framework import serializers
from .models import PostoTrabalho, Maquina, Operacao, Atividade

class PostoTrabalhoSerializer(serializers.ModelSerializer):
    class Meta:
        model = PostoTrabalho
        fields = '__all__'

class MaquinaSerializer(serializers.ModelSerializer):
    class Meta:
        model = Maquina
        fields = '__all__'

class OperacaoSerializer(serializers.ModelSerializer):
    class Meta:
        model = Operacao
        fields = '__all__'

class AtividadeSerializer(serializers.ModelSerializer):
    operacoes = serializers.PrimaryKeyRelatedField(
        many=True, queryset=Operacao.objects.all(), required=False
    )

    class Meta:
        model = Atividade
        fields = [
            "id",
            "nome",
            "data_hora_inicio",
            "data_hora_fim",
            "observacao",
            "posto_trabalho",
            "maquina",
            "operacoes",
        ]
