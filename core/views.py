from rest_framework.viewsets import ModelViewSet
from rest_framework.viewsets import ViewSet
from rest_framework.response import Response
from rest_framework.decorators import action
from rest_framework import status
from rest_framework.exceptions import ValidationError
from .models import PostoTrabalho, Maquina, Operacao, Atividade, Tempos, PostoTrabalho_Py, Atividade_Py, Classificacao, Classificacao_Py,  Maquina_Py, Operacao_Py, Tempos_Py
from django.shortcuts import get_object_or_404
from .serializers import *
from django.db.models import Prefetch
import os
import pandas as pd
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.base import MIMEBase
from io import BytesIO
from django.http import HttpResponse
from django.conf import settings
from email import encoders
import time

# import pyodbc // conecta com o banco de dados, porém incompatível com a versão instalada do pandas
EXCEL_DIR = r'\\192.168.1.28\ENGENHARIA\PUBLICO\00-CRONOANALISE'
EXCEL_DIR_PY = r'\\192.168.1.22\c$\projetos\api_crono\PY_DIRS\EXCEL'
EMAILS_FILE = r'\\192.168.1.22\c$\projetos\api_crono\PY_DIRS\SEND_TO\destinos.txt'
class ClassificacaoViewSet(ViewSet):
    """
    Custom ViewSet para manipularCLassificacao com endpoints específicos.
    """

    # POST personalizado em /api/classificacoes/postocreate/
    @action(detail=False, methods=['post'], url_path='classificacaocreate')
    def create_classificacao(self, request):
        data = request.data

        # Validação dos campos obrigatórios
        if "nome" not in data:
            return Response(
                {"error": "Os campos 'nome'  é obrigatórios."},
                status=status.HTTP_400_BAD_REQUEST
            )

        if not data["nome"].strip():
            return Response(
                {"error": "O campo 'nome' não pode estar vazio."},
                status=status.HTTP_400_BAD_REQUEST
            )

        serializer = ClassificacaoSerializer(data=data)
        serializer.is_valid(raise_exception=True)
        serializer.save()

        return Response(
            {"message": "criado com sucesso!", "data": serializer.data},
            status=status.HTTP_201_CREATED
        )

    # GET personalizado em /api/postos/postolist/
    @action(detail=False, methods=['get'], url_path='classificacaolist')
    def list_classificacao(self, request):
        queryset = Classificacao.objects.all()
        serializer = ClassificacaoSerializer(queryset, many=True)

        return Response(
            {"message": "Lista de CLassificações", "data": serializer.data},
            status=status.HTTP_200_OK
        )

    # PUT personalizado em /api/postos/postoupdate/<id>/
    @action(detail=True, methods=['put'], url_path='classificacaoupdate')
    def update_posto(self, request, pk=None):
        try:
            # Verifica se o objeto existe
            instance = Classificacao.objects.get(pk=pk)
        except Classificacao.DoesNotExist:
            return Response(
                {"error": f"Classificação com ID {pk} não encontrado."},
                status=status.HTTP_404_NOT_FOUND
            )

        # Atualiza os dados com o serializer
        serializer = ClassificacaoSerializer(instance, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        serializer.save()

        return Response(
            {"message": "Classificação atualizado com sucesso!", "data": serializer.data},
            status=status.HTTP_200_OK
        )

    # DELETE personalizado em /api/postos/postodelete/<id>/
    @action(detail=True, methods=['delete'], url_path='classificacaodelete')
    def delete_posto(self, request, pk=None):
        try:
            instance = Classificacao.objects.get(pk=pk)
        except Classificacao.DoesNotExist:
            return Response(
                {"error": f"Classificação com ID {pk} não encontrado."},
                status=status.HTTP_404_NOT_FOUND
            )

        instance.delete()
        return Response(
            {"message": f"Classificação com ID {pk} deletado com sucesso."},
            status=status.HTTP_200_OK
        )


class PostoTrabalhoViewSet(ViewSet):
    """
    Custom ViewSet para manipular Posto de Trabalho com endpoints específicos.
    """

    # POST personalizado em /api/postos/postocreate/
    @action(detail=False, methods=['post'], url_path='postocreate')
    def create_posto(self, request):
        data = request.data

        # Validação dos campos obrigatórios
        if "nome" not in data or "descricao" not in data:
            return Response(
                {"error": "Os campos 'nome' e 'descricao' são obrigatórios."},
                status=status.HTTP_400_BAD_REQUEST
            )

        if not data["nome"].strip():
            return Response(
                {"error": "O campo 'nome' não pode estar vazio."},
                status=status.HTTP_400_BAD_REQUEST
            )

        serializer = PostoTrabalhoSerializer(data=data)
        serializer.is_valid(raise_exception=True)
        serializer.save()

        return Response(
            {"message": "criado com sucesso!", "data": serializer.data},
            status=status.HTTP_201_CREATED
        )

    # GET personalizado em /api/postos/postolist/
    @action(detail=False, methods=['get'], url_path='postolist')
    def list_postos(self, request):
        queryset = PostoTrabalho.objects.all()
        serializer = PostoTrabalhoSerializer(queryset, many=True)

        return Response(
            {"message": "Lista de Postos de Trabalho", "data": serializer.data},
            status=status.HTTP_200_OK
        )

    # PUT personalizado em /api/postos/postoupdate/<id>/
    @action(detail=True, methods=['put'], url_path='postoupdate')
    def update_posto(self, request, pk=None):
        try:
            # Verifica se o objeto existe
            instance = PostoTrabalho.objects.get(pk=pk)
        except PostoTrabalho.DoesNotExist:
            return Response(
                {"error": f"Posto de Trabalho com ID {pk} não encontrado."},
                status=status.HTTP_404_NOT_FOUND
            )

        # Atualiza os dados com o serializer
        serializer = PostoTrabalhoSerializer(instance, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        serializer.save()

        return Response(
            {"message": "Posto de Trabalho atualizado com sucesso!", "data": serializer.data},
            status=status.HTTP_200_OK
        )

    # DELETE personalizado em /api/postos/postodelete/<id>/
    @action(detail=True, methods=['delete'], url_path='postodelete')
    def delete_posto(self, request, pk=None):
        try:
            instance = PostoTrabalho.objects.get(pk=pk)
        except PostoTrabalho.DoesNotExist:
            return Response(
                {"error": f"Posto de Trabalho com ID {pk} não encontrado."},
                status=status.HTTP_404_NOT_FOUND
            )

        instance.delete()
        return Response(
            {"message": f"Posto de Trabalho com ID {pk} deletado com sucesso."},
            status=status.HTTP_200_OK
        )

class MaquinaViewSet(ViewSet):
    """
    Custom ViewSet para manipular Maquina com endpoints específicos.
    """

    # POST personalizado em /api/maquinas/maquinacreate/
    @action(detail=False, methods=['post'], url_path='maquinacreate')
    def create_maquina(self, request):
        data = request.data
        operacoes_ids = data.pop("operacoes", [])

        serializer = MaquinaSerializer(data=data)
        serializer.is_valid(raise_exception=True)
        maquina = serializer.save()

        if operacoes_ids:
            operacoes = Operacao.objects.filter(id__in=operacoes_ids)
            maquina.operacoes.set(operacoes)  # Adiciona a relação ManyToMany

        return Response(
            {"message": "criado com sucesso!", "data": MaquinaSerializer(maquina).data},
            status=status.HTTP_201_CREATED
        )

    @action(detail=True, methods=['put'], url_path='maquinaupdate')
    def update_maquina(self, request, pk=None):
        try:
            maquina = Maquina.objects.get(pk=pk)
        except Maquina.DoesNotExist:
            return Response(
                {"error": f"Máquina com ID {pk} não encontrada."},
                status=status.HTTP_404_NOT_FOUND
            )

        data = request.data
        operacoes_ids = data.pop("operacoes", [])

        serializer = MaquinaSerializer(maquina, data=data, partial=True)
        serializer.is_valid(raise_exception=True)
        maquina = serializer.save()

        if operacoes_ids:
            operacoes = Operacao.objects.filter(id__in=operacoes_ids)
            maquina.operacoes.set(operacoes)

        return Response(
            {"message": f"Máquina com ID {pk} atualizada com sucesso!", "data": MaquinaSerializer(maquina).data},
            status=status.HTTP_200_OK
        )

    @action(detail=False, methods=['get'], url_path='maquinalist')
    def listar_maquinas_com_operacoes(self, request):
        maquinas = Maquina.objects.prefetch_related("operacoes").all()
        data = [
            {
                "id": maquina.id,
                "nome": maquina.nome,
                "descricao": maquina.descricao,
                "operacoes": OperacaoSerializer(maquina.operacoes.all(), many=True).data
            }
            for maquina in maquinas
        ]

        return Response(
            {"message": "Lista de Máquinas e suas Operações", "data": data},
            status=status.HTTP_200_OK
        )

    # DELETE personalizado em /api/maquinas/maquinadelete/<id>/
    @action(detail=True, methods=['delete'], url_path='maquinadelete')
    def delete_maquina(self, request, pk=None):
        try:
            instance = Maquina.objects.get(pk=pk)
        except Maquina.DoesNotExist:
            return Response(
                {"error": f"Máquina com ID {pk} não encontrada."},
                status=status.HTTP_404_NOT_FOUND
            )

        instance.delete()
        return Response(
            {"message": f"Máquina com ID {pk} excluída com sucesso."},
            status=status.HTTP_200_OK
        )

class OperacaoViewSet(ViewSet):
    """
    Custom ViewSet para manipular Operacao com endpoints específicos.
    """

    # POST personalizado em /api/operacoes/operacaocreate/
    @action(detail=False, methods=['post'], url_path='operacaocreate')
    def create_operacao(self, request):
        data = request.data

        # Validação dos campos obrigatórios
        if "nome" not in data or "descricao" not in data or "classificacao" not in data:
            return Response(
                {"error": "Os campos 'nome', 'descricao' e 'classificacao' são obrigatórios."},
                status=status.HTTP_400_BAD_REQUEST
            )

        if not data["nome"].strip():
            return Response(
                {"error": "O campo 'nome' não pode estar vazio."},
                status=status.HTTP_400_BAD_REQUEST
            )

        serializer = OperacaoSerializer(data=data)
        serializer.is_valid(raise_exception=True)
        serializer.save()

        return Response(
            {"message": "criado com sucesso!", "data": serializer.data},
            status=status.HTTP_201_CREATED
        )

    # GET personalizado em /api/operacoes/operacaolist/
    @action(detail=False, methods=['get'], url_path='operacaolist')
    def list_operacao(self, request):
        queryset = Operacao.objects.all()
        serializer = OperacaoSerializer(queryset, many=True)

        return Response(
            {"message": "Lista de Operações ", "data": serializer.data},
            status=status.HTTP_200_OK
        )

    # PUT personalizado em /api/operacoes/operacaoupdate/<id>/
    @action(detail=True, methods=['put'], url_path='operacaoupdate')
    def update_operacao(self, request, pk=None):
        try:
            instance = Operacao.objects.get(pk=pk)
        except Operacao.DoesNotExist:
            return Response(
                {"error": f"Operacao com ID {pk} não encontrado."},
                status=status.HTTP_404_NOT_FOUND
            )
        
        serializer = OperacaoSerializer(instance, data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()

        return Response(
            {"message": f"Operacao com ID {pk} atualizado com sucesso!", "data": serializer.data},
            status=status.HTTP_200_OK
        )

    # DELETE personalizado em /api/operacoes/operacaodelete/<id>/
    @action(detail=True, methods=['delete'], url_path='operacaodelete')
    def delete_operacao(self, request, pk=None):
        try:
            instance = Operacao.objects.get(pk=pk)
        except Operacao.DoesNotExist:
            return Response(
                {"error": f"Operação com ID {pk} não encontrada."},
                status=status.HTTP_404_NOT_FOUND
            )

        # Verifica se a operação está vinculada a alguma máquina
        if instance.maquinas.exists():  # Use o related_name correto
            return Response(
                {"error": f"A operação '{instance.nome}' está vinculada a máquinas e não pode ser excluída."},
                status=status.HTTP_400_BAD_REQUEST
            )

        instance.delete()
        return Response(
            {"message": f"Operação com ID {pk} excluída com sucesso."},
            status=status.HTTP_200_OK
        )


class AtividadeViewSet(ModelViewSet):
    queryset = Atividade.objects.prefetch_related(
        Prefetch("tempos_set", queryset=Tempos.objects.select_related("operacao"))
    ).select_related("posto_trabalho", "maquina")
    serializer_class = AtividadeSerializer
   
    def create(self, request, *args, **kwargs):
        data = request.data
        data_str = str(data)
    
    # Cria e salva o arquivo .txt
        with open('data_output.txt', 'w') as file:
            file.write(data_str)


        # Validação de campos obrigatórios
        required_fields = ["nome", "data_hora_inicio", "data_hora_fim", "posto_trabalho", "maquina", "tempo_total"]
        for field in required_fields:
            if field not in data:
                return Response(
                    {"error": f"O campo '{field}' é obrigatório."},
                    status=status.HTTP_400_BAD_REQUEST,
                )


        # Validar se os IDs fornecidos existem
        try:
            posto_trabalho = PostoTrabalho.objects.get(id=data["posto_trabalho"])
            maquina = Maquina.objects.get(id=data["maquina"])
        except PostoTrabalho.DoesNotExist:
            return Response({"error": "Posto de Trabalho inválido."}, status=status.HTTP_400_BAD_REQUEST)
        except Maquina.DoesNotExist:
            return Response({"error": "Máquina inválida."}, status=status.HTTP_400_BAD_REQUEST)

        # Criar a atividade sem operações inicialmente
        serializer = self.get_serializer(data=data)
        serializer.is_valid(raise_exception=True)
        atividade = serializer.save()

        tempos_data = []
        if "operacoes" in data:
            operacoes_ids = data["operacoes"]
            tempos = data["tempos"]

            for operacao_id, tempo in zip(operacoes_ids, tempos):
                operacao = get_object_or_404(Operacao, id=operacao_id)
                tempo_obj = Tempos.objects.create(atividade=atividade, operacao=operacao, tempo=tempo)
                tempos_data.append({
                    "operacao": operacao.nome,
                    "descricao da operação": operacao.descricao,
                    "tempo (segundos)": tempo_obj.tempo,
                    "classificacao": operacao.classificacao.nome,
    
                })

        # Criar DataFrame para a aba principal
        df_atividade = pd.DataFrame([{
            "id": atividade.id,
            "nome": atividade.nome,
            "data_hora_inicio": atividade.data_hora_inicio,
            "data_hora_fim": atividade.data_hora_fim,
            "observacao": atividade.observacao,
            "posto_trabalho": atividade.posto_trabalho.nome,
            "maquina": atividade.maquina.nome,
            "tempo_total": atividade.tempo_total,
        }])

        # Criar DataFrame para a aba de operações
        df_tempos = pd.DataFrame(tempos_data)

        # Criar o nome do arquivo
        file_path = os.path.join(EXCEL_DIR, f"atividade_{atividade.id}.xlsx")

        # Criar e salvar o Excel
        with pd.ExcelWriter(file_path, engine="xlsxwriter") as writer:
            df_atividade.to_excel(writer, sheet_name="Atividade", index=False)
            df_tempos.to_excel(writer, sheet_name="Operações", index=False)


        return Response(
            {"message": "criado com sucesso!"},
            status=status.HTTP_201_CREATED,
        )

    def list(self, request, *args, **kwargs):
        queryset = self.get_queryset()
        data = []

        for atividade in queryset:
           
            tempos_data = [
                {
                    "operacao": tempo.operacao.nome,
                    "tempo": tempo.tempo,
                }
                for tempo in atividade.tempos_set.all()
            ]

            data.append({
                "id": atividade.id,
                "nome": atividade.nome,
                "data_hora_inicio": atividade.data_hora_inicio,
                "data_hora_fim": atividade.data_hora_fim,
                "observacao": atividade.observacao,
                "posto_trabalho": atividade.posto_trabalho.nome,
                "maquina": atividade.maquina.nome,
                "tempos": tempos_data,
                "tempo_total": atividade.tempo_total,
                
            })

        return Response(
            {"message": "Lista de atividades", "data": data},
            status=status.HTTP_200_OK,
        )

class ClassificacaoPyViewSet(ViewSet):
    """
    Custom ViewSet para manipularCLassificacao com endpoints específicos.
    """

    # POST personalizado em /api/classificacoes/postocreate/
    @action(detail=False, methods=['post'], url_path='classificacaocreate')
    def create_classificacao_py(self, request):
        data = request.data

        # Validação dos campos obrigatórios
        if "nome" not in data:
            return Response(
                {"error": "Os campos 'nome'  é obrigatórios."},
                status=status.HTTP_400_BAD_REQUEST
            )

        if not data["nome"].strip():
            return Response(
                {"error": "O campo 'nome' não pode estar vazio."},
                status=status.HTTP_400_BAD_REQUEST
            )

        serializer = ClassificacaoPySerializer(data=data)
        serializer.is_valid(raise_exception=True)
        serializer.save()

        return Response(
            {"message": "criado com sucesso!", "data": serializer.data},
            status=status.HTTP_201_CREATED
        )

    # GET personalizado em /api/postos/postolist/
    @action(detail=False, methods=['get'], url_path='classificacaolist')
    def list_classificacao(self, request):
        queryset = Classificacao_Py.objects.all()
        serializer = ClassificacaoPySerializer(queryset, many=True)

        return Response(
            {"message": "Lista de CLassificações", "data": serializer.data},
            status=status.HTTP_200_OK
        )

    # PUT personalizado em /api/postos/postoupdate/<id>/
    @action(detail=True, methods=['put'], url_path='classificacaoupdate')
    def update_posto(self, request, pk=None):
        try:
            # Verifica se o objeto existe
            instance = Classificacao_Py.objects.get(pk=pk)
        except Classificacao_Py.DoesNotExist:
            return Response(
                {"error": f"Classificação com ID {pk} não encontrado."},
                status=status.HTTP_404_NOT_FOUND
            )

        # Atualiza os dados com o serializer
        serializer = ClassificacaoPySerializer(instance, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        serializer.save()

        return Response(
            {"message": "Classificação atualizado com sucesso!", "data": serializer.data},
            status=status.HTTP_200_OK
        )

    # DELETE personalizado em /api/postos/postodelete/<id>/
    @action(detail=True, methods=['delete'], url_path='classificacaodelete')
    def delete_posto(self, request, pk=None):
        try:
            instance = Classificacao_Py.objects.get(pk=pk)
        except Classificacao_Py.DoesNotExist:
            return Response(
                {"error": f"Classificação com ID {pk} não encontrado."},
                status=status.HTTP_404_NOT_FOUND
            )

        instance.delete()
        return Response(
            {"message": f"Classificação com ID {pk} deletado com sucesso."},
            status=status.HTTP_200_OK
        )


class PostoTrabalhoPyViewSet(ViewSet):
    """
    Custom ViewSet para manipular Posto de Trabalho com endpoints específicos.
    """

    # POST personalizado em /api/postos/postocreate/
    @action(detail=False, methods=['post'], url_path='postocreate')
    def create_posto(self, request):
        data = request.data

        # Validação dos campos obrigatórios
        if "nome" not in data or "descricao" not in data:
            return Response(
                {"error": "Os campos 'nome' e 'descricao' são obrigatórios."},
                status=status.HTTP_400_BAD_REQUEST
            )

        if not data["nome"].strip():
            return Response(
                {"error": "O campo 'nome' não pode estar vazio."},
                status=status.HTTP_400_BAD_REQUEST
            )

        serializer = PostoTrabalhoPySerializer(data=data)
        serializer.is_valid(raise_exception=True)
        serializer.save()

        return Response(
            {"message": "criado com sucesso!", "data": serializer.data},
            status=status.HTTP_201_CREATED
        )

    # GET personalizado em /api/postos/postolist/
    @action(detail=False, methods=['get'], url_path='postolist')
    def list_postos(self, request):
        queryset = PostoTrabalho_Py.objects.all()
        serializer = PostoTrabalhoPySerializer(queryset, many=True)

        return Response(
            {"message": "Lista de Postos de Trabalho", "data": serializer.data},
            status=status.HTTP_200_OK
        )

    # PUT personalizado em /api/postos/postoupdate/<id>/
    @action(detail=True, methods=['put'], url_path='postoupdate')
    def update_posto(self, request, pk=None):
        try:
            # Verifica se o objeto existe
            instance = PostoTrabalho_Py.objects.get(pk=pk)
        except PostoTrabalho_Py.DoesNotExist:
            return Response(
                {"error": f"Posto de Trabalho com ID {pk} não encontrado."},
                status=status.HTTP_404_NOT_FOUND
            )

        # Atualiza os dados com o serializer
        serializer = PostoTrabalhoPySerializer(instance, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        serializer.save()

        return Response(
            {"message": "Posto de Trabalho atualizado com sucesso!", "data": serializer.data},
            status=status.HTTP_200_OK
        )

    # DELETE personalizado em /api/postos/postodelete/<id>/
    @action(detail=True, methods=['delete'], url_path='postodelete')
    def delete_posto(self, request, pk=None):
        try:
            instance = PostoTrabalho_Py.objects.get(pk=pk)
        except PostoTrabalho_Py.DoesNotExist:
            return Response(
                {"error": f"Posto de Trabalho com ID {pk} não encontrado."},
                status=status.HTTP_404_NOT_FOUND
            )

        instance.delete()
        return Response(
            {"message": f"Posto de Trabalho com ID {pk} deletado com sucesso."},
            status=status.HTTP_200_OK
        )

class MaquinaPyViewSet(ViewSet):
    """
    Custom ViewSet para manipular Maquina com endpoints específicos.
    """

    # POST personalizado em /api/maquinas/maquinacreate/
    @action(detail=False, methods=['post'], url_path='maquinacreate')
    def create_maquina(self, request):
        data = request.data
        operacoes_ids = data.pop("operacoes", [])

        serializer = MaquinaPySerializer(data=data)
        serializer.is_valid(raise_exception=True)
        maquina = serializer.save()

        if operacoes_ids:
            operacoes = Operacao_Py.objects.filter(id__in=operacoes_ids)
            maquina.operacoes.set(operacoes)  # Adiciona a relação ManyToMany

        return Response(
            {"message": "criado com sucesso!", "data": MaquinaPySerializer(maquina).data},
            status=status.HTTP_201_CREATED
        )

    @action(detail=True, methods=['put'], url_path='maquinaupdate')
    def update_maquina(self, request, pk=None):
        try:
            maquina = Maquina_Py.objects.get(pk=pk)
        except Maquina_Py.DoesNotExist:
            return Response(
                {"error": f"Máquina com ID {pk} não encontrada."},
                status=status.HTTP_404_NOT_FOUND
            )

        data = request.data
        operacoes_ids = data.pop("operacoes", [])

        serializer = MaquinaPySerializer(maquina, data=data, partial=True)
        serializer.is_valid(raise_exception=True)
        maquina = serializer.save()

        if operacoes_ids:
            operacoes = Operacao_Py.objects.filter(id__in=operacoes_ids)
            maquina.operacoes.set(operacoes)

        return Response(
            {"message": f"Máquina com ID {pk} atualizada com sucesso!", "data": MaquinaPySerializer(maquina).data},
            status=status.HTTP_200_OK
        )

    @action(detail=False, methods=['get'], url_path='maquinalist')
    def listar_maquinas_com_operacoes(self, request):
        maquinas = Maquina_Py.objects.prefetch_related("operacoes").all()
        data = [
            {
                "id": maquina.id,
                "nome": maquina.nome,
                "descricao": maquina.descricao,
                "operacoes": OperacaoPySerializer(maquina.operacoes.all(), many=True).data
            }
            for maquina in maquinas
        ]

        return Response(
            {"message": "Lista de Máquinas e suas Operações", "data": data},
            status=status.HTTP_200_OK
        )

    # DELETE personalizado em /api/maquinas/maquinadelete/<id>/
    @action(detail=True, methods=['delete'], url_path='maquinadelete')
    def delete_maquina(self, request, pk=None):
        try:
            instance = Maquina_Py.objects.get(pk=pk)
        except Maquina_Py.DoesNotExist:
            return Response(
                {"error": f"Máquina com ID {pk} não encontrada."},
                status=status.HTTP_404_NOT_FOUND
            )

        instance.delete()
        return Response(
            {"message": f"Máquina com ID {pk} excluída com sucesso."},
            status=status.HTTP_200_OK
        )

class OperacaoPyViewSet(ViewSet):
    """
    Custom ViewSet para manipular Operacao com endpoints específicos.
    """

    # POST personalizado em /api/operacoes/operacaocreate/
    @action(detail=False, methods=['post'], url_path='operacaocreate')
    def create_operacao(self, request):
        data = request.data

        # Validação dos campos obrigatórios
        if "nome" not in data or "descricao" not in data or "classificacao" not in data:
            return Response(
                {"error": "Os campos 'nome', 'descricao' e 'classificacao' são obrigatórios."},
                status=status.HTTP_400_BAD_REQUEST
            )

        if not data["nome"].strip():
            return Response(
                {"error": "O campo 'nome' não pode estar vazio."},
                status=status.HTTP_400_BAD_REQUEST
            )

        serializer = OperacaoPySerializer(data=data)
        serializer.is_valid(raise_exception=True)
        serializer.save()

        return Response(
            {"message": "criado com sucesso!", "data": serializer.data},
            status=status.HTTP_201_CREATED
        )

    # GET personalizado em /api/operacoes/operacaolist/
    @action(detail=False, methods=['get'], url_path='operacaolist')
    def list_operacao(self, request):
        queryset = Operacao_Py.objects.all()
        serializer = OperacaoPySerializer(queryset, many=True)

        return Response(
            {"message": "Lista de Operações ", "data": serializer.data},
            status=status.HTTP_200_OK
        )

    # PUT personalizado em /api/operacoes/operacaoupdate/<id>/
    @action(detail=True, methods=['put'], url_path='operacaoupdate')
    def update_operacao(self, request, pk=None):
        try:
            instance = Operacao_Py.objects.get(pk=pk)
        except Operacao_Py.DoesNotExist:
            return Response(
                {"error": f"Operacao com ID {pk} não encontrado."},
                status=status.HTTP_404_NOT_FOUND
            )
        
        serializer = OperacaoPySerializer(instance, data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()

        return Response(
            {"message": f"Operacao com ID {pk} atualizado com sucesso!", "data": serializer.data},
            status=status.HTTP_200_OK
        )

    # DELETE personalizado em /api/operacoes/operacaodelete/<id>/
    @action(detail=True, methods=['delete'], url_path='operacaodelete')
    def delete_operacao(self, request, pk=None):
        try:
            instance = Operacao_Py.objects.get(pk=pk)
        except Operacao_Py.DoesNotExist:
            return Response(
                {"error": f"Operação com ID {pk} não encontrada."},
                status=status.HTTP_404_NOT_FOUND
            )

        # Verifica se a operação está vinculada a alguma máquina
        if instance.maquinas.exists():  # Use o related_name correto
            return Response(
                {"error": f"A operação '{instance.nome}' está vinculada a máquinas e não pode ser excluída."},
                status=status.HTTP_400_BAD_REQUEST
            )

        instance.delete()
        return Response(
            {"message": f"Operação com ID {pk} excluída com sucesso."},
            status=status.HTTP_200_OK
        )


class AtividadePyViewSet(ModelViewSet):
    queryset = Atividade_Py.objects.prefetch_related(
        Prefetch("tempos_set", queryset=Tempos_Py.objects.select_related("operacao"))
    ).select_related("posto_trabalho", "maquina")
    serializer_class = AtividadePySerializer
   
    def create(self, request, *args, **kwargs):
        data = request.data
        data_str = str(data)
    
    # Cria e salva o arquivo .txt
        with open('data_output.txt', 'w') as file:
            file.write(data_str)


        # Validação de campos obrigatórios
        required_fields = ["nome", "data_hora_inicio", "data_hora_fim", "posto_trabalho", "maquina", "tempo_total"]
        for field in required_fields:
            if field not in data:
                return Response(
                    {"error": f"O campo '{field}' é obrigatório."},
                    status=status.HTTP_400_BAD_REQUEST,
                )


        # Validar se os IDs fornecidos existem
        try:
            posto_trabalho = PostoTrabalho_Py.objects.get(id=data["posto_trabalho"])
            maquina = Maquina_Py.objects.get(id=data["maquina"])
        except PostoTrabalho_Py.DoesNotExist:
            return Response({"error": "Posto de Trabalho inválido."}, status=status.HTTP_400_BAD_REQUEST)
        except Maquina_Py.DoesNotExist:
            return Response({"error": "Máquina inválida."}, status=status.HTTP_400_BAD_REQUEST)

        # Criar a atividade sem operações inicialmente
        serializer = self.get_serializer(data=data)
        serializer.is_valid(raise_exception=True)
        atividade = serializer.save()

        tempos_data = []
        if "operacoes" in data:
            operacoes_ids = data["operacoes"]
            tempos = data["tempos"]

            for operacao_id, tempo in zip(operacoes_ids, tempos):
                operacao = get_object_or_404(Operacao_Py, id=operacao_id)
                tempo_obj = Tempos_Py.objects.create(atividade=atividade, operacao=operacao, tempo=tempo)
                tempos_data.append({
                    "operacao": operacao.nome,
                    "descricao da operação": operacao.descricao,
                    "tempo (segundos)": tempo_obj.tempo,
                    "classificacao": operacao.classificacao.nome,
    
                })

        # Criar DataFrame para a aba principal
        df_atividade = pd.DataFrame([{
            "id": atividade.id,
            "nome": atividade.nome,
            "data_hora_inicio": atividade.data_hora_inicio,
            "data_hora_fim": atividade.data_hora_fim,
            "observacao": atividade.observacao,
            "posto_trabalho": atividade.posto_trabalho.nome,
            "maquina": atividade.maquina.nome,
            "tempo_total": atividade.tempo_total,
        }])

        # Criar DataFrame para a aba de operações
        df_tempos = pd.DataFrame(tempos_data)

        # Criar o nome do arquivo
        file_path = os.path.join(EXCEL_DIR_PY, f"atividade_{atividade.id}.xlsx")

        # Criar e salvar o Excel
        with pd.ExcelWriter(file_path, engine="xlsxwriter") as writer:
            df_atividade.to_excel(writer, sheet_name="Atividade", index=False)
            df_tempos.to_excel(writer, sheet_name="Operações", index=False)
        
        # Ler os e-mails do arquivo txt
         # Substitua pelo caminho correto do arquivo
        with open(EMAILS_FILE, "r") as f:
            destinatarios = [email.strip() for email in f.read().split(",") if email.strip()]
        for destinatario in destinatarios:
            self.enviar_email(destinatario, file_path)
            

        return Response(
            {"message": "criado com sucesso!"},
            status=status.HTTP_201_CREATED,
        )

    def list(self, request, *args, **kwargs):
        queryset = self.get_queryset()
        data = []

        for atividade in queryset:
           
            tempos_data = [
                {
                    "operacao": tempo.operacao.nome,
                    "tempo": tempo.tempo,
                }
                for tempo in atividade.tempos_set.all()
            ]

            data.append({
                "id": atividade.id,
                "nome": atividade.nome,
                "data_hora_inicio": atividade.data_hora_inicio,
                "data_hora_fim": atividade.data_hora_fim,
                "observacao": atividade.observacao,
                "posto_trabalho": atividade.posto_trabalho.nome,
                "maquina": atividade.maquina.nome,
                "tempos": tempos_data,
                "tempo_total": atividade.tempo_total,
                
            })

        return Response(
            {"message": "Lista de atividades", "data": data},
            status=status.HTTP_200_OK,
        )
    
    def enviar_email(self, destinatario, anexo_path):
        remetente = "tiago.leal@robustecsa.com.py"
        senha = "poouwmshmaerasbp"

        try:
            with smtplib.SMTP("smtp.gmail.com", 587) as servidor:
                servidor.starttls()
                servidor.login(remetente, senha)
                # Configuração do e-mail
                msg = MIMEMultipart()
                msg["From"] = remetente
                msg["To"] = destinatario
                msg["Subject"] = "Relatório de Atividade"

                # Corpo do e-mail
                corpo = f"Segue em anexo o relatório da atividade realizado em cronoanálise."
                msg.attach(MIMEText(corpo, "plain"))

                # Anexar o arquivo
                with open(anexo_path, "rb") as anexo:
                    part = MIMEBase("application", "octet-stream")
                    part.set_payload(anexo.read())
                    encoders.encode_base64(part)
                    part.add_header("Content-Disposition", f"attachment; filename={os.path.basename(anexo_path)}")
                    msg.attach(part)

                # Enviar email para o destinatário
                servidor.sendmail(remetente, destinatario, msg.as_string())

                print("E-mails enviados com sucesso!")
        except Exception as e:
            print(f"Erro ao enviar e-mail: {e}")