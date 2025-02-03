from rest_framework.viewsets import ModelViewSet
from rest_framework.viewsets import ViewSet
from rest_framework.response import Response
from rest_framework.decorators import action
from rest_framework import status
from rest_framework.exceptions import ValidationError
from .models import PostoTrabalho, Maquina, Operacao, Atividade, Tempos
from .serializers import *
from django.db.models import Prefetch

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
            {"message": "Posto criado com sucesso!", "data": serializer.data},
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

        serializer = MaquinaSerializer(data=data)
        serializer.is_valid(raise_exception=True)
        serializer.save()

        return Response(
            {"message": "Maquina criada com sucesso!", "data": serializer.data},
            status=status.HTTP_201_CREATED
        )

    # GET personalizado em /api/maquinas/maquinalist/
    @action(detail=False, methods=['get'], url_path='maquinalist')
    def list_postos(self, request):
        queryset = Maquina.objects.all()
        serializer = MaquinaSerializer(queryset, many=True)

        return Response(
            {"message": "Lista de Maquinas de Trabalho", "data": serializer.data},
            status=status.HTTP_200_OK
        )

    # PUT personalizado em /api/maquinas/maquinaupdate/<id>/
    @action(detail=True, methods=['put'], url_path='maquinaupdate')
    def update_posto(self, request, pk=None):
        try:
            instance = Maquina.objects.get(pk=pk)
        except Maquina.DoesNotExist:
            return Response(
                {"error": f"Maquina com ID {pk} não encontrado."},
                status=status.HTTP_404_NOT_FOUND
            )

        serializer = MaquinaSerializer(instance, data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()

        return Response(
            {"message": f"Maquina com ID {pk} atualizado com sucesso!", "data": serializer.data},
            status=status.HTTP_200_OK
        )

    # DELETE personalizado em /api/maquinas/maquinadelete/<id>/
    @action(detail=True, methods=['delete'], url_path='maquinadelete')
    def delete_posto(self, request, pk=None):
        try:
            instance = Maquina.objects.get(pk=pk)
        except Maquina.DoesNotExist:
            return Response(
                {"error": f"Maquina  com ID {pk} não encontrado."},
                status=status.HTTP_404_NOT_FOUND
            )

        instance.delete()
        return Response(
            {"message": f"Maquina com ID {pk} deletado com sucesso."},
            status=status.HTTP_200_OK
        )

class OperacaoViewSet(ViewSet):
    """
    Custom ViewSet para manipular Operacao com endpoints específicos.
    """

    # POST personalizado em /api/operacoes/operacaocreate/
    @action(detail=False, methods=['post'], url_path='operacaocreate')
    def create_posto(self, request):
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
            {"message": "Operacao criada com sucesso!", "data": serializer.data},
            status=status.HTTP_201_CREATED
        )

    # GET personalizado em /api/operacoes/operacaolist/
    @action(detail=False, methods=['get'], url_path='operacaolist')
    def list_postos(self, request):
        queryset = Operacao.objects.all()
        serializer = OperacaoSerializer(queryset, many=True)

        return Response(
            {"message": "Lista de Operações ", "data": serializer.data},
            status=status.HTTP_200_OK
        )

    # PUT personalizado em /api/operacoes/operacaoupdate/<id>/
    @action(detail=True, methods=['put'], url_path='operacaoupdate')
    def update_posto(self, request, pk=None):
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
    def delete_posto(self, request, pk=None):
        try:
            instance = Operacao.objects.get(pk=pk)
        except Operacao.DoesNotExist:
            return Response(
                {"error": f"operacao  com ID {pk} não encontrado."},
                status=status.HTTP_404_NOT_FOUND
            )

        instance.delete()
        return Response(
            {"message": f"operacao com ID {pk} deletado com sucesso."},
            status=status.HTTP_200_OK
        )

class AtividadeViewSet(ModelViewSet):
    queryset = Atividade.objects.prefetch_related(
        Prefetch("tempos_set", queryset=Tempos.objects.select_related("operacao"))
    ).select_related("posto_trabalho", "maquina")
    serializer_class = AtividadeSerializer
   
    def create(self, request, *args, **kwargs):
        data = request.data

        # Validação de campos obrigatórios
        required_fields = ["nome", "data_hora_inicio", "data_hora_fim", "posto_trabalho", "maquina"]
        for field in required_fields:
            if field not in data:
                return Response(
                    {"error": f"O campo '{field}' é obrigatório."},
                    status=status.HTTP_400_BAD_REQUEST,
                )

        # Validar se data_hora_fim > data_hora_inicio
        if data["data_hora_fim"] <= data["data_hora_inicio"]:
            return Response(
                {"error": "A 'data_hora_fim' deve ser posterior à 'data_hora_inicio'."},
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

        # Criar entradas no modelo Tempos para cada operação fornecida
        if "operacoes" in data:
            operacoes_ids = data["operacoes"]
            tempos = data["tempos"]
            id = 0
            for operacao_id in operacoes_ids:
                tp_op = tempos[id]
                try:
                    operacao = Operacao.objects.get(id=operacao_id)
                    Tempos.objects.create(atividade=atividade, operacao=operacao, tempo = tp_op)
                    id = id+1
                except Operacao.DoesNotExist:
                    raise ValidationError({"operacoes": f"Operação inválida com ID {operacao_id}."})

        return Response(
            {"message": "Atividade criada com sucesso!", "data": serializer.data},
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
            })

        return Response(
            {"message": "Lista de atividades", "data": data},
            status=status.HTTP_200_OK,
        )