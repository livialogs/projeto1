console.log("Arquivo script.js foi carregado com sucesso!");

// Define a url da api de serviços
const API_SERVICOS_URL = 'http://127.0.0.1:8000/api/servicos/';

// Pega o elemento da lista no HTML
const listaServicosElement = document.getElementById('lista-servicos');

console.log("Arquivo script.js foi carregado com sucesso 2!");


// Função assíncrona pra buscar os dados
async function carregarServicos() {
    // Limpa a lista inicial
    listaServicosElement.innerHTML = '';

    try {
        // Faz a chamada de rede para a API
        const response = await fetch(API_SERVICOS_URL);
        // Converte a resposta em JSON
        const servicos = await response.json();

        // Para cada serviço na lista, cria um item HTML
        servicos.forEach(servico => {
            const itemLista = document.createElement('li');
            itemLista.innerHTML = `
                <h3>${servico.nome}</h3>
                <p>${servico.descricao}</p>
                <p>Preço: R$ ${servico.preco}</p>
            `;
            listaServicosElement.appendChild(itemLista);
        });
    } catch (error) {
        console.error('Erro ao carregar serviços:', error);
        listaServicosElement.innerHTML = '<li>Não foi possível carregar os serviços.</li>';
    }
}

// Chama a função pra carregar os serviços quando a página abre
carregarServicos();