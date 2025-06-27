# Este arquivo funciona como a "alfândega" ou a camada de "tradução" da nossa API.
# Sua principal responsabilidade é converter os dados complexos do Django (objetos de modelo)
# para um formato simples que pode ser enviado pela internet (JSON), e vice-versa.
# Ele também é responsável por validar os dados que chegam do front-end.

# Importa a base de serializers do Django REST Framework (DRF)
from rest_framework import serializers 
# Importa os nossos modelos do banco de dados para que os serializers saibam qual a estrutura dos dados
from core.models import Servico, User, Agendamento


# -----------------------------------------------------------------------------
# SERIALIZERS PARA OS MODELOS PRINCIPAIS (Leitura de Dados Públicos)
# -----------------------------------------------------------------------------

class ServicoSerializer(serializers.ModelSerializer):
    """
    Serializa os dados do modelo Servico para serem expostos na API.
    É um serializer simples, focado em mostrar os dados de um serviço.
    """
    class Meta:
        # Define que este serializer está ligado ao nosso modelo 'Servico'
        model = Servico
        # Define exatamente quais campos do modelo 'Servico' serão incluídos no JSON final.
        fields = ['id', 'nome', 'descricao', 'duracao_minutos', 'preco']


class FuncionarioSerializer(serializers.ModelSerializer):
    """
    Serializa dados de usuários que são funcionários, expondo apenas informações públicas.
    Importante para popular a lista de funcionários na tela de agendamento.
    """
    class Meta:
        # Liga este serializer ao modelo 'User', o mesmo modelo de cliente,
        # mas vamos selecionar campos diferentes.
        model = User
        # Especifica que, para um funcionário, queremos mostrar apenas o seu ID, 
        # nome e sobrenome, e a foto, e não dados sensíveis como o e-mail ou senha.
        fields = ['id', 'first_name', 'last_name', 'foto_perfil']


# -----------------------------------------------------------------------------
# SERIALIZER PARA REGISTRO DE USUÁRIO
# -----------------------------------------------------------------------------

class UserRegisterSerializer(serializers.ModelSerializer):
    """
    Responsável por receber os dados de registro de um novo usuário
    e garantir que a conta seja criada de forma segura.
    """
    class Meta:
        model = User
        # Define os campos que o front-end DEVE enviar no corpo da requisição POST.
        fields = ['id', 'username', 'email', 'password', 'first_name', 'last_name']
        
        # Uma configuração de segurança crucial do DRF.
        extra_kwargs = {
            'password': {'write_only': True} # 'write_only' significa: "Este campo pode ser enviado para a API (escrita), 
                                             # mas NUNCA deve ser incluído na resposta da API (leitura)".
                                             # Isso evita que a senha, mesmo criptografada, seja exposta.
        }

    def create(self, validated_data):
        """
        Sobrescrevemos o método 'create' padrão do ModelSerializer para usar a função
        correta de criação de usuário do Django, que lida com a criptografia da senha.
        Este método é chamado automaticamente pela view quando o serializer.save() é invocado.
        """
        # Usamos User.objects.create_user() em vez de User.objects.create().
        # A função 'create_user' é a que corretamente faz o HASH (criptografa) da senha
        # antes de salvá-la no banco de dados. Este é um passo fundamental de segurança.
        user = User.objects.create_user(
            username=validated_data['username'],
            email=validated_data['email'],
            password=validated_data['password'],
            first_name=validated_data['first_name'],
            last_name=validated_data['last_name']
        )
        
        # Retorna a instância do usuário recém-criado.
        return user


# -----------------------------------------------------------------------------
# SERIALIZERS PARA AGENDAMENTO (Leitura e Escrita Separadas)
# -----------------------------------------------------------------------------

class AgendamentoSerializer(serializers.ModelSerializer):
    """
    Serializa os dados de um agendamento para LEITURA. 
    É otimizado para exibir informações de forma amigável no front-end,
    buscando nomes de campos relacionados em vez de apenas os IDs.
    """
    # Cria um campo virtual 'servico_nome'.
    # 'read_only=True' significa que este campo é apenas para a resposta da API, não para entrada.
    # 'source='servico.nome'' diz ao serializer: "Para preencher este campo, olhe para o
    # objeto 'servico' relacionado a este agendamento e pegue o valor do seu atributo 'nome'".
    servico_nome = serializers.CharField(source='servico.nome', read_only=True)
    
    # Faz o mesmo para o funcionário, mas usa o método 'get_full_name' do modelo User.
    funcionario_nome = serializers.CharField(source='funcionario.get_full_name', read_only=True)

    class Meta:
        model = Agendamento
        # Define os campos que serão mostrados na lista de "meus agendamentos".
        fields = ['id', 'servico_nome', 'funcionario_nome', 'data_hora', 'status']


class AgendamentoCreateSerializer(serializers.ModelSerializer):
    """
    Serializa os dados para CRIAÇÃO de um novo agendamento. 
    É otimizado para receber apenas a informação mínima e necessária do front-end.
    """
    class Meta:
        model = Agendamento
        # Para criar um agendamento, o front-end só precisa enviar os IDs do serviço
        # e do funcionário, além da data. O 'cliente' será associado automaticamente na view
        # a partir do usuário que está logado, garantindo a segurança.
        fields = ['servico', 'funcionario', 'data_hora']