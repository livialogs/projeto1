document.addEventListener('DOMContentLoaded', () => {
    // 1. O "SEGURANÇA": Verifica se o usuário tem o crachá (token)
    const accessToken = localStorage.getItem('accessToken');

    // Se NÃO existir token, o usuário não está logado.
    if (!accessToken) {
        // Manda um alerta e redireciona p a página de login
        alert('Você precisa estar logado para ver esta página.');
        window.location.href = 'login.html';
        return; // Para a execução do script aqui.
    }

    // Se o script continuou, significa que o usuário tem um token
    // Agora busca os dados na API:

    const listaAgendamentosElement = document.getElementById('lista-agendamentos');
    const API_URL = 'http://127.0.0.1:8000/api/meus-agendamentos/';

    async function carregarMeusAgendamentos() {
        listaAgendamentosElement.innerHTML = ''; // Limpa a lista

        try {
            // 2. A CHAMADA AUTENTICADA: Faz a chamada para a API, mas desta vez...
            const response = await fetch(API_URL, {
                method: 'GET',
                headers: {
                    // ...é enviado o "crachá" no cabeçalho de autorização!
                    'Authorization': `Bearer ${accessToken}`
                }
            });

            if (response.ok) {
                const agendamentos = await response.json();
                
                if (agendamentos.length === 0) {
                    listaAgendamentosElement.innerHTML = '<li>Você ainda não tem agendamentos.</li>';
                    return;
                }

                agendamentos.forEach(agendamento => {
                    const itemLista = document.createElement('li');
                    // Formata a data pra ficar mais legível
                    const dataFormatada = new Date(agendamento.data_hora).toLocaleString('pt-BR');

                    itemLista.innerHTML = `
                        <strong>Serviço:</strong> ${agendamento.servico_nome} com ${agendamento.funcionario_nome}
                        <br>
                        <strong>Data:</strong> ${dataFormatada}
                        <br>
                        <strong>Status:</strong> ${agendamento.status}
                    `;
                    listaAgendamentosElement.appendChild(itemLista);
                });

            } else {
                // Se o token for inválido ou expirado, a API retornará um erro 401 ou 403
                console.error('Erro de autorização:', response.status);
                listaAgendamentosElement.innerHTML = '<li>Ocorreu um erro ao buscar seus agendamentos. Tente fazer o login novamente.</li>';
            }
        } catch (error) {
            console.error('Erro de rede:', error);
            listaAgendamentosElement.innerHTML = '<li>Não foi possível conectar ao servidor.</li>';
        }
    }

    // Chama a função para carregar os agendamentos.
    carregarMeusAgendamentos();
});