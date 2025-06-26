from rest_framework import generics
from rest_framework.generics import ListAPIView
from rest_framework.permissions import AllowAny # Permite que qualquer um se registre
from core.models import Servico, User
from .serializers import (ServicoSerializer, FuncionarioSerializer, UserRegisterSerializer, AgendamentoSerializer,
    AgendamentoCreateSerializer)
from rest_framework.permissions import IsAuthenticated
from .serializers import AgendamentoSerializer
from core.models import Servico, User, Agendamento
from .serializers import AgendamentoCreateSerializer


class ServicosListView(ListAPIView):
    queryset = Servico.objects.all()
    serializer_class = ServicoSerializer

class FuncionariosListView(ListAPIView):
    queryset = User.objects.filter(tipo_usuario='FUNCIONARIO')
    serializer_class = FuncionarioSerializer


class UserRegisterView(generics.CreateAPIView):
    queryset = User.objects.all()
    # Qualquer um pode acessar esta view para se registrar
    permission_classes = (AllowAny,)
    serializer_class = UserRegisterSerializer

class MeusAgendamentosListView(generics.ListAPIView):
    serializer_class = AgendamentoSerializer
    permission_classes = [IsAuthenticated] # 1. SÓ usuários logados podem ver

    def get_queryset(self):
        # 2. Filtra os agendamentos pra mostrar só os do usuário que fez a requisição
        return Agendamento.objects.filter(cliente=self.request.user)

class AgendamentoCreateView(generics.CreateAPIView):
    serializer_class = AgendamentoCreateSerializer
    permission_classes = [IsAuthenticated]

    def perform_create(self, serializer):
        # Força que o 'cliente' do agendamento seja o usuário logado
        serializer.save(cliente=self.request.user)