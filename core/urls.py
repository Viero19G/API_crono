from rest_framework.routers import DefaultRouter
from .views import *
from django.urls import path, include


router = DefaultRouter()
router.register('postos', PostoTrabalhoViewSet, basename='postos')
router.register('maquinas', MaquinaViewSet, basename='maquinas')
router.register('operacoes', OperacaoViewSet, basename='operacoes')
router.register('atividades', AtividadeViewSet, basename='atividades')

urlpatterns = [
    path('', include(router.urls)),
]
