// Função para formatar o valor com duas casas decimais
function formatarValorDecimal(valor) {
    var valorFormatado = parseFloat(valor).toFixed(2);
    return valorFormatado.replace('.', '.');
}

// Variável para controlar o contador de produtos
let produtoCounter = 0;

// Função para calcular e atualizar o valor total com base nos valores unitários e quantidades
function atualizarValorTotal() {
    const produtosItems = document.querySelectorAll('.produto-item');
    let valorTotal = 0;

    produtosItems.forEach(item => {
        const quantidade = parseInt(item.querySelector('.quantidade-input').value) || 0;
        const valorUnitario = parseFloat(item.querySelector('.valor-unitario-input').value) || 0;
        const subtotal = quantidade * valorUnitario;
        valorTotal += subtotal;
    });

    const valorTotalInput = document.getElementById('valor_total');
    valorTotalInput.value = formatarValorDecimal(valorTotal);
}

// Função para atualizar o valor unitário quando um produto é selecionado
function setupProdutoEventListeners(produtoItem) {
    const selectProduto = produtoItem.querySelector('.produto-select');
    const inputValorUnitario = produtoItem.querySelector('.valor-unitario-input');
    const inputQuantidade = produtoItem.querySelector('.quantidade-input');
    
    selectProduto.addEventListener('change', function() {
        const selectedOption = this.options[this.selectedIndex];
        const valor = selectedOption.getAttribute('data-valor');
        inputValorUnitario.value = valor || '';
        atualizarValorTotal();
    });
    
    inputQuantidade.addEventListener('input', atualizarValorTotal);
}

// Função para adicionar um novo produto
function adicionarProduto() {
    produtoCounter++;
    
    // Clonar o primeiro item de produto
    const produtosContainer = document.getElementById('produtos-container');
    const produtoTemplate = produtosContainer.querySelector('.produto-item').cloneNode(true);
    
    // Atualizar os IDs e limpar valores
    const selectProduto = produtoTemplate.querySelector('.produto-select');
    const inputQuantidade = produtoTemplate.querySelector('.quantidade-input');
    const inputValorUnitario = produtoTemplate.querySelector('.valor-unitario-input');
    const btnRemover = produtoTemplate.querySelector('.btn-remover-produto');
    
    selectProduto.id = `id_produto_${produtoCounter}`;
    selectProduto.value = '';
    
    inputQuantidade.id = `quantidade_${produtoCounter}`;
    inputQuantidade.value = '1';
    
    inputValorUnitario.id = `valor_unitario_${produtoCounter}`;
    inputValorUnitario.value = '';
    
    // Mostrar o botão de remover
    btnRemover.style.display = 'block';
    
    // Adicionar o novo item ao container
    produtosContainer.appendChild(produtoTemplate);
    
    // Configurar event listeners para o novo item
    setupProdutoEventListeners(produtoTemplate);
    
    // Configurar o botão de remover
    btnRemover.addEventListener('click', function() {
        produtoTemplate.remove();
        atualizarValorTotal();
        atualizarBotoesRemover();
    });
}

// Função para atualizar a visibilidade dos botões de remover
function atualizarBotoesRemover() {
    const produtosItems = document.querySelectorAll('.produto-item');
    
    // Se só tiver um produto, esconder o botão de remover
    if (produtosItems.length === 1) {
        produtosItems[0].querySelector('.btn-remover-produto').style.display = 'none';
    } else {
        // Caso contrário, mostrar todos os botões de remover
        produtosItems.forEach(item => {
            item.querySelector('.btn-remover-produto').style.display = 'block';
        });
    }
}

// Função para formatar a data como "YYYY-MM-DD"
function formatDate(date) {
    const year = date.getFullYear();
    const month = String(date.getMonth() + 1).padStart(2, '0');
    const day = String(date.getDate()).padStart(2, '0');
    return `${year}-${month}-${day}`;
}

// Função para preencher a data atual no campo de data
document.addEventListener('DOMContentLoaded', function() {
    const dataInput = document.getElementById('data');
    const today = new Date();
    const formattedDate = formatDate(today);
    dataInput.value = formattedDate;
});

function formatarValor(valor) {
    // Verifica se o valor é válido (número)
    if (isNaN(valor)) {
        return; // Sai da função se não for um número
    }

    // Formata o valor para moeda brasileira (R$)
    const valorFormatado = parseFloat(valor).toLocaleString('pt-BR', {
        style: 'currency',
        currency: 'BRL'
    });

    return valorFormatado;
}

// Função para exibir a data atual
function exibirDataAtual() {
    // Criar um novo objeto Date (que representa a data e hora atuais)
    var dataAtual = new Date();

    // Obter o dia, mês e ano da data atual
    var dia = dataAtual.getDate();
    var mes = dataAtual.getMonth() + 1; // O mês é baseado em zero (janeiro = 0), então adicionamos 1
    var ano = dataAtual.getFullYear();

    // Formatar a data como "DD/MM/AAAA" (por exemplo, "14/04/2024")
    var dataFormatada = dia + '/' + mes + '/' + ano;

    // Obter o elemento HTML onde queremos exibir a data atual
    var elementoDataAtual = document.getElementById('dataAtual');

    // Atualizar o conteúdo do elemento com a data formatada
    if (elementoDataAtual) {
        elementoDataAtual.textContent = "Data Atual: " + dataFormatada;
    }
}

// Inicialização quando o DOM estiver carregado
document.addEventListener('DOMContentLoaded', function() {
    // Inicializar o primeiro item de produto
    const primeiroProdutoItem = document.querySelector('.produto-item');
    setupProdutoEventListeners(primeiroProdutoItem);
    
    // Configurar o botão de adicionar produto
    const btnAdicionarProduto = document.getElementById('adicionar-produto');
    btnAdicionarProduto.addEventListener('click', adicionarProduto);
    
    // Inicializar o contador com base no estado atual da página
    produtoCounter = document.querySelectorAll('.produto-item').length - 1;
    
    // Configurar validação de contato
    document.getElementById('id_contato').addEventListener('input', function() {
        var input = this;
        var erro_contato = document.getElementById('erro_contato');
        if (input.value.length !== 11) {
            input.classList.add('is-invalid');
            erro_contato.style.display = 'block';
        } else {
            input.classList.remove('is-invalid');
            erro_contato.style.display = 'none';
        }
    });

    // Configurar validação de CPF/CNPJ
    document.getElementById('id_cpf_cnpj').addEventListener('input', function() {
        var input = this;
        var erro_contato = document.getElementById('erro_cpf_cnpj');
        if (input.value.length < 11 || input.value.length > 14) {
            input.classList.add('is-invalid');
            erro_contato.style.display = 'block';
        } else {
            input.classList.remove('is-invalid');
            erro_contato.style.display = 'none';
        }
    });
    
    // Configurar busca de cliente por CPF/CNPJ
    var cpfCnpjInput = document.getElementById('id_cpf_cnpj');
    var nomeClienteInput = document.getElementById('id_nome_cliente');
    var contatoInput = document.getElementById('id_contato');
    
    if (cpfCnpjInput) {
        var url = cpfCnpjInput.getAttribute('data-url');

        cpfCnpjInput.addEventListener('change', function() {
            var cpf_cnpj = this.value;
            if (cpf_cnpj) {
                fetch(url + '?cpf_cnpj=' + cpf_cnpj)
                    .then(response => response.json())
                    .then(data => {
                        if (data.error) {
                            alert('Cliente não encontrado!');
                        } else {
                            // Preencher os campos automaticamente
                            nomeClienteInput.value = data.nome_cliente;
                            contatoInput.value = data.contato;
                        }
                    })
                    .catch(error => console.error('Erro:', error));
            }
        });
    }
    
    // Validação do formulário
    document.getElementById('criarPedidoForm').addEventListener('submit', function(event) {
        // Verificar se pelo menos um produto foi selecionado
        const produtos = document.querySelectorAll('.produto-select');
        let produtoSelecionado = false;
        
        produtos.forEach(selectProduto => {
            if (selectProduto.value) {
                produtoSelecionado = true;
            }
        });
        
        if (!produtoSelecionado) {
            alert('Por favor, selecione pelo menos um produto.');
            event.preventDefault();
            return false;
        }
        
        // Adicionar um campo escondido com o produto principal (para compatibilidade)
        const primeiroProduto = document.querySelector('#id_produto_0');
        if (primeiroProduto && primeiroProduto.value) {
            const hiddenProduto = document.createElement('input');
            hiddenProduto.type = 'hidden';
            hiddenProduto.name = 'produto';
            hiddenProduto.value = primeiroProduto.value;
            this.appendChild(hiddenProduto);
            
            const hiddenQuantidade = document.createElement('input');
            hiddenQuantidade.type = 'hidden';
            hiddenQuantidade.name = 'quantidade';
            hiddenQuantidade.value = document.querySelector('#quantidade_0').value;
            this.appendChild(hiddenQuantidade);
            
            const hiddenValorUnitario = document.createElement('input');
            hiddenValorUnitario.type = 'hidden';
            hiddenValorUnitario.name = 'valor_unitario';
            hiddenValorUnitario.value = document.querySelector('#valor_unitario_0').value;
            this.appendChild(hiddenValorUnitario);
        }
    });
    
    // Calcular o valor total inicialmente
    atualizarValorTotal();
    
    // Exibir data atual
    exibirDataAtual();
});
