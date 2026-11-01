
    // 1. Função de Busca Instantânea nos Cards
    function filtrarProdutos() {
        const input = document.getElementById('buscaInput').value.toLowerCase();
        const cards = document.querySelectorAll('.product-card');

        cards.forEach(card => {
            const nome = card.querySelector('.product-name').textContent.toLowerCase();
            if (nome.includes(input)) {
                card.style.display = "flex";
            } else {
                card.style.display = "none";
            }
        });
    }

    // 2. Criar e inserir dinamicamente a barra de pesquisa e botão de compartilhar no HTML via JS
    window.addEventListener('DOMContentLoaded', () => {
        const containerHeader = document.querySelector('.header');
        
        const barraBuscaHTML = `
            <div style="margin-top: 15px;">
                <input type="text" id="buscaInput" onkeyup="filtrarProdutos()" placeholder="🔍 Pesquisar oferta..." style="width: 100%; padding: 10px; border-radius: 8px; border: 1px solid #334155; background: #0f172a; color: white; box-sizing: border-box;">
            </div>
        `;
        containerHeader.insertAdjacentHTML('beforeend', barraBuscaHTML);
    });