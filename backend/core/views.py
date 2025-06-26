from django.shortcuts import render

# core/views.py
from django.shortcuts import render
from .models import Servico, Agendamento

def home_page_view(request):
    servicos = Servico.objects.all()
    meus_agendamentos = []

    # Se o usuário estiver logado, pega os agendamentos dele
    if request.user.is_authenticated and request.user.tipo_usuario == 'CLIENTE':
        meus_agendamentos = Agendamento.objects.filter(cliente=request.user)

    context = {
        'servicos': servicos,
        'meus_agendamentos': meus_agendamentos
    }
    return render(request, 'home.html', context)