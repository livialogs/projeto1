# Projeto de Agendamento de Massoterapia - Lívia Maria Dutra

Este projeto é uma aplicação web completa para um sistema de agendamento de massoterapia, desenvolvido como parte da avaliação da disciplina de Desenvolvimento Web.
A aplicação segue uma arquitetura de front-end e back-end desacoplados, que se comunicam através de uma API REST.


## Principais Funcionalidades

O sistema permite que usuários realizem as seguintes ações:


* **Visualização de Serviços:** Usuários podem ver uma lista de todos os serviços de massoterapia oferecidos, com descrição e preço.
* **Autenticação Segura:** Clientes podem se registrar e fazer login na plataforma. A autenticação é gerenciada via tokens JWT (JSON Web Tokens).
* **Agendamento de Consultas:** Clientes autenticados podem agendar um serviço com um profissional em uma data e hora específicas.
* **Dashboard do Cliente:** Clientes logados podem ver uma lista de seus agendamentos futuros e passados.
* **Painel Administrativo:** Uma área de administração robusta para gerenciar usuários, serviços e todos os agendamentos.


## Características do Sistema Desenvolvido

### Tecnologias Utilizadas

* **Back-end:** Python 3, Django, Django REST Framework (para a API), Simple JWT (para autenticação via token).
* **Front-end:** HTML5, CSS3 e JavaScript puro (Vanilla JS), consumindo a API REST através da Fetch API.
* **Banco de Dados:** SQLite 3 (banco de dados padrão do Django para desenvolvimento).
* **Versionamento:** Git e GitHub.

### Arquitetura Adotada

O projeto foi estruturado seguindo os princípios da **Arquitetura em Camadas (Layered Architecture)**, com uma separação entre o cliente (front-end) e o servidor (back-end).


* **Back-end (Django):** Desenvolvido com o framework Django, que implementa o padrão arquitetural MVT (Model-View-Template). Esta é uma arquitetura em camadas que separa as responsabilidades:
    * **Model:** Define a estrutura dos dados, os relacionamentos e as regras de negócio essenciais (`core/models.py`). Foi utilizado um **Modelo de Classe Base** para garantir consistência e evitar repetição de código entre as entidades.
    * **View:** Contém a lógica de negócio de cada endpoint, recebendo as requisições, interagindo com os modelos e orquestrando a resposta (`core/api/views.py`).
    * **Apresentação da API:** Os **Serializers** do Django REST Framework atuam como a camada de apresentação, convertendo os objetos do Django para o formato JSON. O acesso aos dados é abstraído pelo ORM do Django, que é uma implementação robusta do **Padrão de Repositório**.

* **Front-end (HTML/JS):** Desenvolvido como uma aplicação de página única (SPA) em espírito ( tecnicamente ele navega entre arquivos HTML distintos com recarregamentos de página), utilizando HTML5, CSS3 e JavaScript puro. O JavaScript é responsável por:
    * Consumir a API REST de forma assíncrona usando a **Fetch API**.
    * Manipular o DOM para exibir os dados dinamicamente na tela.
    * Gerenciar o estado de autenticação do usuário através de tokens JWT guardados no `localStorage`.

## Instruções de Execução

Para executar o projeto localmente, siga os passos abaixo.

**Pré-requisitos:**
* Python 3.x instalado
* Git instalado

**Passos:**

1.  **Clone o repositório:**
    ```bash
    git clone https://github.com/livialogs/projeto1
    ```

2.  **Navegue até a pasta do back-end:**
    ```bash
    cd nome-da-pasta-do-projeto/backend
    ```

3.  **Crie e ative um ambiente virtual:**
    ```bash
    # Criar o venv
    python -m venv venv
    # Ativar no Windows
    venv\Scripts\activate
    # Ativar no macOS/Linux
    # source venv/bin/activate
    ```

4.  **Instale as dependências:**
    ```bash
    pip install -r requirements.txt
    ```

5.  **Aplique as migrações do banco de dados:**
    ```bash
    python manage.py migrate
    ```

6.  **Crie seu próprio usuário administrador:**
    ```bash
    python manage.py createsuperuser
    ```
    *(Siga as instruções no terminal para definir seu e-mail e senha)*

7.  **Inicie o Servidor do Back-end:**
    ```bash
    python manage.py runserver
    ```
    *Deixe este terminal rodando.*

8.  **Inicie o Servidor do Front-end:**
    * Abra um **NOVO** terminal.
    * Navegue até a pasta do front-end: `cd ../frontend` (o `../` volta uma pasta)
    * Inicie o servidor web simples:
        ```bash
        python -m http.server 8001
        ```
    * *Deixe este segundo terminal rodando.*

9.  **Acesse a Aplicação:**
    * A aplicação front-end estará disponível em: `http://localhost:8001`

### Primeiros Passos Após a Instalação

1.  Após iniciar os dois servidores, acesse o **Painel de Administração** em `http://127.0.0.1:8000/admin/`.
2.  Faça login com o **superusuário** que você acabou de criar no passo 6.
3.  Pelo painel, crie alguns **Serviços** e alguns **Usuários** (do tipo 'Cliente' e 'Funcionário') para popular o sistema com dados de teste.
4.  Agora você pode acessar o front-end em `http://localhost:8001` para testar o fluxo de login e agendamento com os usuários que criou.