from rest_framework import serializers
from .models import PostoTrabalho, Maquina, Operacao, Atividade, Tempos, Classificacao, PostoTrabalho_Py, Maquina_Py, Tempos_Py, Operacao_Py, Atividade_Py, Classificacao_Py

class PostoTrabalhoSerializer(serializers.ModelSerializer):
    class Meta:
        model = PostoTrabalho
        fields = '__all__'

class MaquinaSerializer(serializers.ModelSerializer):
    operacoes = serializers.PrimaryKeyRelatedField(
        many=True, queryset=Operacao.objects.all(), required=False
    )  

    class Meta:
        model = Maquina
        fields = '__all__'


class OperacaoSerializer(serializers.ModelSerializer):
    class Meta:
        model = Operacao
        fields = '__all__'

class ClassificacaoSerializer(serializers.ModelSerializer):
    class Meta:
        model = Classificacao
        fields = '__all__'

class TempoSerializer(serializers.ModelSerializer):
    class Meta:
        model = Tempos
        fields = '__all__'

class AtividadeSerializer(serializers.ModelSerializer):
     class Meta:
        model = Atividade
        fields = '__all__'



class PostoTrabalhoPySerializer(serializers.ModelSerializer):
    class Meta:
        model = PostoTrabalho_Py
        fields = '__all__'

class MaquinaPySerializer(serializers.ModelSerializer):
    operacoes = serializers.PrimaryKeyRelatedField(
        many=True, queryset=Operacao_Py.objects.all(), required=False
    )  

    class Meta:
        model = Maquina_Py
        fields = '__all__'


class OperacaoPySerializer(serializers.ModelSerializer):
    class Meta:
        model = Operacao_Py
        fields = '__all__'

class ClassificacaoPySerializer(serializers.ModelSerializer):
    class Meta:
        model = Classificacao_Py
        fields = '__all__'

class TempoPySerializer(serializers.ModelSerializer):
    class Meta:
        model = Tempos_Py
        fields = '__all__'

class AtividadePySerializer(serializers.ModelSerializer):
     class Meta:
        model = Atividade_Py
        fields = '__all__'