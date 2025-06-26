// Executa o script quando o HTML tiver carregado totalmente
document.addEventListener('DOMContentLoaded', () => {

    // --- O "Segurança": Verifica se o usuário esta logado ---
    const accessToken = localStorage.getItem('accessToken');
    if (!accessToken) {
        alert('Você precisa estar logado para agendar.');
        window.location.href = 'login.html';
        return; // Para a execução do script se não tiver login
    }

    // --- Seleciona os elementos do formulário no HTML ---
    const form = document.getElementById('agendamento-form');
    const servicoSelect = document.getElementById('servico-select');
    const funcionarioSelect = document.getElementById('funcionario-select');
    const dataHoraInput = document.getElementById('data-hora-input');
    const mensagemStatusDiv = document.getElementById('mensagem-status');

    // --- Funções para buscar dados e popular os menus de seleção ---

    // Função para buscar e preencher a lista de serviços
    async function popularServicos() {
        const response = await fetch('http://127.0.0.1:8000/api/servicos/');
        const servicos = await response.json();
        servicoSelect.innerHTML = '<option value="">Selecione um serviço</option>'; // Limpa e adiciona a opção padrão
        servicos.forEach(servico => {
            const option = document.createElement('option');
            option.value = servico.id; // O valor do option vai ser o ID do serviço
            option.textContent = `${servico.nome} (R$ ${servico.preco})`; // O texto visível
            servicoSelect.appendChild(option);
        });
    }

    // Função pra buscar e preencher lista de funcionários
    async function popularFuncionarios() {
        const response = await fetch('http://127.0.0.1:8000/api/funcionarios/');
        const funcionarios = await response.json();
        funcionarioSelect.innerHTML = '<option value="">Selecione um profissional</option>'; // Limpa e adiciona a opção padrão
        funcionarios.forEach(func => {
            const option = document.createElement('option');
            option.value = func.id; // O valor do option vai ser o ID do funcionário
            option.textContent = `${func.first_name} ${func.last_name}`; // O texto visível
            funcionarioSelect.appendChild(option);
        });
    }

    // --- Lógica para o envio do formulário ---

    // Adiciona o fofoqueiro para o envio do formulário
    form.addEventListener('submit', async (event) => {
        event.preventDefault(); // Impede o recarregamento da página

        // Pega os valores selecionados pelo usuário
        const servicoId = servicoSelect.value;
        const funcionarioId = funcionarioSelect.value;
        const dataHora = dataHoraInput.value;

        // Limpa mensagens antigas
        mensagemStatusDiv.textContent = '';
        mensagemStatusDiv.style.color = 'black';

        try {
            // Faz a chamada POST para a API, enviando os dados e o token de autorização
            const response = await fetch('http://127.0.0.1:8000/api/agendamentos/', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                    'Authorization': `Bearer ${accessToken}` // Envia o crachá/token
                },
                // Corpo da requisição com os dados do formulário
                body: JSON.stringify({
                    servico: servicoId,
                    funcionario: funcionarioId,
                    data_hora: new Date(dataHora).toISOString() // Converte a data para o formato que a API ta esperando
                })
            });

            if (response.ok) {
                mensagemStatusDiv.textContent = 'Agendamento criado com sucesso!';
                mensagemStatusDiv.style.color = 'green';
                form.reset(); // Limpa o formulário
            } else {
                const errorData = await response.json();
                // Mostra o erro que vem da API (ex: "horário indisponível")
                mensagemStatusDiv.textContent = `Erro: ${JSON.stringify(errorData)}`;
                mensagemStatusDiv.style.color = 'red';
            }
        } catch (error) {
            console.error('Erro de rede:', error);
            mensagemStatusDiv.textContent = 'Não foi possível conectar ao servidor.';
            mensagemStatusDiv.style.color = 'red';
        }
    });

    // --- Execução Inicial ---
    
    // Chama as funções para preencher os dropdowns quando a página carrega
    popularServicos();
    popularFuncionarios();
});