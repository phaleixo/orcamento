document.addEventListener('DOMContentLoaded', function() {
    // Botões de filtro de período
    const filterWeek = document.getElementById('filter-week');
    const filterMonth = document.getElementById('filter-month');
    const filterYear = document.getElementById('filter-year');
    
    if (filterWeek && filterMonth && filterYear) {
        // Adicionar eventos de clique
        filterWeek.addEventListener('click', function() {
            window.location.href = updateQueryParam('periodo', 'semana');
        });
        
        filterMonth.addEventListener('click', function() {
            window.location.href = updateQueryParam('periodo', 'mes');
        });
        
        filterYear.addEventListener('click', function() {
            window.location.href = updateQueryParam('periodo', 'ano');
        });
        
        // Definir o botão ativo com base no parâmetro da URL
        const urlParams = new URLSearchParams(window.location.search);
        const periodo = urlParams.get('periodo');
        
        // Remover a classe ativa de todos os botões
        filterWeek.classList.remove('active');
        filterMonth.classList.remove('active');
        filterYear.classList.remove('active');
        
        // Adicionar a classe ativa ao botão correto
        if (periodo === 'mes') {
            filterMonth.classList.add('active');
        } else if (periodo === 'ano') {
            filterYear.classList.add('active');
        } else {
            // Default é semana
            filterWeek.classList.add('active');
        }
    }
    
    // Função para atualizar parâmetros de URL sem perder os outros parâmetros existentes
    function updateQueryParam(key, value) {
        const url = new URL(window.location.href);
        url.searchParams.set(key, value);
        return url.toString();
    }
}); 