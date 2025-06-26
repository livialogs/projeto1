# core/admin.py
from django.contrib import admin
from .models import User, Servico, Agendamento

admin.site.register(User)
admin.site.register(Servico)
admin.site.register(Agendamento)