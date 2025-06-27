from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import User, Servico, Agendamento

# Esta classe customiza como o modelo 'User' aparece no admin
class CustomUserAdmin(UserAdmin):
    # O fieldsets controla como os campos são organizados na página de edição
    # Pegando a organização padrão do UserAdmin e adicionando a nossa seção
    fieldsets = UserAdmin.fieldsets + (
        ('Campos Customizados', {'fields': ('tipo_usuario', 'foto_perfil')}),
    )

# Registra os modelos normais como antes
admin.site.register(Servico)
admin.site.register(Agendamento)

# Registra modelo User, mas usando a classe customizada que foi criada
admin.site.register(User, CustomUserAdmin)