from django.urls import path
from .views import ServicosListView, FuncionariosListView, UserRegisterView
from .views import MeusAgendamentosListView
from .views import AgendamentoCreateView

# Lista de URLs deste app
urlpatterns = [
    # Se a URL for 'servicos/', chame a view ServicosListView
    path('servicos/', ServicosListView.as_view(), name='lista-servicos'),

    # Se a URL for 'funcionarios/', chame a view FuncionariosListView
    path('funcionarios/', FuncionariosListView.as_view(), name='lista-funcionarios'),

    path('users/register/', UserRegisterView.as_view(), name='user-register'),

    path('meus-agendamentos/', MeusAgendamentosListView.as_view(), name='meus-agendamentos'),

    path('agendamentos/', AgendamentoCreateView.as_view(), name='criar-agendamento'),
]