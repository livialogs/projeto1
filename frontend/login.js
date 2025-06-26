// Espera o HTML carregar completamente antes de executar o script
document.addEventListener('DOMContentLoaded', () => {
    // Pega os elementos do formulário no HTML pelos IDs
    const loginForm = document.getElementById('login-form');
    const emailInput = document.getElementById('email');
    const passwordInput = document.getElementById('password');
    const errorMessageDiv = document.getElementById('error-message');

    // Fofoqueiro addEventListener vai vigiar o loginForm (que pegamos do html), submit é a fofoca que ele está esperando. Ele ignora cliques, mouse etc mas quando o usuario 'submit', ou seja, clica 'Entrar', o fofoqueiro vai agir
    loginForm.addEventListener('submit', async (event) => {
        // Previne o comportamento padrão do formulário (recarregar a página
        event.preventDefault();

        // Pega os valores digitados pelo usuário
        const email = emailInput.value;
        const password = passwordInput.value;

        // Limpa mensagens de erro antigas
        errorMessageDiv.textContent = '';

        try {
            // Faz a chamada fetch para a API de token do Django
            const response = await fetch('http://127.0.0.1:8000/api/token/', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                // Converte os dados do formulário pra formato JSON
                body: JSON.stringify({ email: email, password: password }),
            });

            // Se a resposta da API der certo (status 200-299)
            if (response.ok) {
                const data = await response.json();
                
                // GUARDA OS TOKENS NO NAVEGADOR!!!!!!!
                localStorage.setItem('accessToken', data.access);
                localStorage.setItem('refreshToken', data.refresh);

                // Redirecionar o usuário para a página de agendamentos
                window.location.href = 'meus-agendamentos.html'; 
            } else {
                // Se a resposta for erro (ex: 401 Unauthorized), mostra um erro
                errorMessageDiv.textContent = 'Email ou senha inválidos. Tente novamente.';
            }
        } catch (error) {
            // Se tiver erro de rede (API desligada etc)
            console.error('Erro de rede:', error);
            errorMessageDiv.textContent = 'Não foi possível conectar ao servidor. Verifique sua conexão.';
        }
    });
});