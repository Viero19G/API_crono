from rest_framework import serializers
from .models import PostoTrabalho, Maquina, Operacao, Atividade, Tempos

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

class TempoSerializer(serializers.ModelSerializer):
    class Meta:
        model = Tempos
        fields = '__all__'

class AtividadeSerializer(serializers.ModelSerializer):
     class Meta:
        model = Atividade
        fields = '__all__'