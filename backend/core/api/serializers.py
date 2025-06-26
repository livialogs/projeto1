from rest_framework import serializers
from core.models import Servico, User
from core.models import Agendamento # Agendamento importado

class ServicoSerializer(serializers.ModelSerializer):
    class Meta:
        model = Servico
        fields = ['id', 'nome', 'descricao', 'duracao_minutos', 'preco']

class FuncionarioSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'first_name', 'last_name', 'foto_perfil']


class UserRegisterSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        # Campos que o front-end vai enviar no JSON
        fields = ['id', 'username', 'email', 'password', 'first_name', 'last_name']
        # Configuração extra: a senha só pode ser escrita (enviada), nunca lida (devolvida na resposta)
        extra_kwargs = {'password': {'write_only': True}}

    def create(self, validated_data):
        # Este método é chamado quando .save() é executado na view
        # Cuida de criar o usuário com a senha criptografada corretamente
        user = User.objects.create_user(
            username=validated_data['username'],
            email=validated_data['email'],
            password=validated_data['password'],
            first_name=validated_data['first_name'],
            last_name=validated_data['last_name']
        )
        
        return user
    

# Serializer para LER/LISTAR agendamentos 
class AgendamentoSerializer(serializers.ModelSerializer):
    # 'source' pega o nome de campos de tabelas relacionadas
    servico_nome = serializers.CharField(source='servico.nome', read_only=True)
    funcionario_nome = serializers.CharField(source='funcionario.get_full_name', read_only=True)

    class Meta:
        model = Agendamento
        # Os campos pra mostrar na lista de "meus agendamentos"
        fields = ['id', 'servico_nome', 'funcionario_nome', 'data_hora', 'status']

# Serializer para CRIAR um novo agendamento
class AgendamentoCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Agendamento
        # O front-end só precisa nos enviar os IDs e a data
        # O 'cliente' vai ser adicionado automaticamente na view
        fields = ['servico', 'funcionario', 'data_hora']

class AgendamentoCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Agendamento
        # O front-end só precisa enviar os IDs e a data
        fields = ['servico', 'funcionario', 'data_hora']