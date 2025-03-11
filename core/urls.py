from rest_framework.routers import DefaultRouter
from .views import *
from django.urls import path, include


router = DefaultRouter()
router.register('postos', PostoTrabalhoViewSet, basename='postos')
router.register('maquinas', MaquinaViewSet, basename='maquinas')
router.register('operacoes', OperacaoViewSet, basename='operacoes')
router.register('atividades', AtividadeViewSet, basename='atividades')
router.register('classificacoes', ClassificacaoViewSet, basename='classificacoes')
router.register('py/postos', PostoTrabalhoPyViewSet, basename='postos')
router.register('py/maquinas', MaquinaPyViewSet, basename='maquinas')
router.register('py/operacoes', OperacaoPyViewSet, basename='operacoes')
router.register('py/atividades', AtividadePyViewSet, basename='atividades')
router.register('py/classificacoes', ClassificacaoPyViewSet, basename='classificacoes')


urlpatterns = [
    path('', include(router.urls)),
]
