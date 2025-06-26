# core/models.py
import uuid
from django.db import models
from django.contrib.auth.models import AbstractUser

class EntidadeBase(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    created_at = models.DateTimeField(auto_now_add=True, editable=False)
    updated_at = models.DateTimeField(auto_now=True, editable=False)

    class Meta:
        abstract = True
        ordering = ['-created_at']

class User(AbstractUser, EntidadeBase):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    TIPO_USUARIO_CHOICES = (("CLIENTE", "Cliente"), ("FUNCIONARIO", "Funcionário"))

    email = models.EmailField(unique=True) # Email será o login
    tipo_usuario = models.CharField(max_length=15, choices=TIPO_USUARIO_CHOICES, default="CLIENTE")
    foto_perfil = models.ImageField(upload_to='perfil_fotos/', null=True, blank=True)

    USERNAME_FIELD = 'email' # Define o email como campo de login
    REQUIRED_FIELDS = ['username', 'first_name'] # Campos pedidos ao criar superuser

    def __str__(self):
        return self.email

class Servico(EntidadeBase):
    nome = models.CharField(max_length=100)
    descricao = models.TextField()
    duracao_minutos = models.IntegerField(help_text="Duração do serviço em minutos")
    preco = models.DecimalField(max_digits=7, decimal_places=2)

    def __str__(self):
        return self.nome

class Agendamento(EntidadeBase):
    STATUS_CHOICES = (("AGENDADO", "Agendado"), ("CONCLUIDO", "Concluído"), ("CANCELADO", "Cancelado"))

    cliente = models.ForeignKey(User, on_delete=models.CASCADE, related_name="agendamentos_como_cliente")
    funcionario = models.ForeignKey(User, on_delete=models.CASCADE, related_name="agendamentos_como_funcionario", limit_choices_to={'tipo_usuario': 'FUNCIONARIO'})
    servico = models.ForeignKey(Servico, on_delete=models.CASCADE)
    data_hora = models.DateTimeField()
    status = models.CharField(max_length=15, choices=STATUS_CHOICES, default="AGENDADO")

    def __str__(self):
        return f"{self.servico.nome} com {self.funcionario.first_name} em {self.data_hora.strftime('%d/%m/%Y %H:%M')}"