// Função para formatar o valor com duas casas decimais
function formatarValorDecimal(valor) {
    var valorFormatado = parseFloat(valor).toFixed(2);
    return valorFormatado.replace('.', '.');
}

// Função para calcular e atualizar o valor total com base nos valores unitários e quantidades
function atualizarValorTotal() {
    const inputsQuantidade = document.querySelectorAll('[name^="quantidade"]');
    const inputsValorUnitario = document.querySelectorAll('[name^="valor_unitario"]');
    let valorTotal = 0;

    inputsQuantidade.forEach((inputQuantidade, index) => {
        const quantidade = parseInt(inputQuantidade.value) || 0;
        const valorUnitario = parseFloat(inputsValorUnitario[index].value.replace(',', '.')) || 0; // Substituir vírgula por ponto
        const subtotal = quantidade * valorUnitario;
        valorTotal += subtotal;
    });

    const valorTotalInput = document.getElementById('valor_total');
    valorTotalInput.value = formatarValorDecimal(valorTotal);
}

// Adicionar event listener para calcular o valor total quando as quantidades ou valores unitários mudam
document.addEventListener('DOMContentLoaded', function() {
    const inputsQuantidade = document.querySelectorAll('[name^="quantidade"]');
    const inputsValorUnitario = document.querySelectorAll('[name^="valor_unitario"]');

    inputsQuantidade.forEach(inputQuantidade => {
        inputQuantidade.addEventListener('input', atualizarValorTotal);
    });

    inputsValorUnitario.forEach(inputValorUnitario => {
        inputValorUnitario.addEventListener('input', atualizarValorTotal);
    });

    // Calcular o valor total inicialmente ao carregar a página
    atualizarValorTotal();
});


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

    // Atualiza o valor no campo de entrada
    document.getElementById('valor_unitario').value = valorFormatado;
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
elementoDataAtual.textContent = "Data Atual: " + dataFormatada;
}

// Chamar a função para exibir a data atual quando a página terminar de carregar
window.onload = exibirDataAtual;

document.addEventListener('DOMContentLoaded', function() {
    var adicionarProdutoBtn = document.getElementById('adicionarProdutoBtn');
    adicionarProdutoBtn.addEventListener('click', adicionarProduto);
});

// Função para validar o formulário antes de submeter
$(document).ready(function () {
    $('#btnSalvarPedido').click(function () {
        // Resetar o alerta de erro
        $('#alertaErro').hide();
        $('#listaErros').empty();

        // Validar o formulário manualmente
        var nomeCliente = $('#id_nome_cliente').val();
        var contato = $('#id_contato').val();
        var cpfCnpj = $('#id_cpf_cnpj').val();
        var produto = $('input[name="produto"]').val();
        var quantidade = $('input[name="quantidade"]').val();
        var valorUnitario = $('input[name="valor_unitario"]').val();
        var descricaoImpresso = $('#descricao_pedido').val();
        var descricaoPedido = $('textarea[name="descricao_pedido"]').val();

        var errors = [];

        if (nomeCliente.trim() === '') {
            errors.push('Nome do Cliente é obrigatório.');
        }
        if (contato.trim().length < 11) {
            errors.push('Contato é obrigatório.');
        }
        if (cpfCnpj.trim().length < 14) {
            errors.push('CPF/CNPJ é obrigatório.');
        }
        if (produto.trim() === '') {
            errors.push('Produto é obrigatório.');
        }
        if (quantidade.trim().length < 1) {
            errors.push('Quantidade é obrigatória.');
        }
        if (valorUnitario.trim() === '') {
            errors.push('Valor Unitário é obrigatório.');
        }
        if (descricaoImpresso.trim() === '') {
            errors.push('Descrição do Impresso é obrigatória.');
        }
        if (descricaoPedido.trim() === '') {
            errors.push('Descrição do Pedido é obrigatória.');
        }

        // Exibir o alerta de erro se houver problemas
        if (errors.length > 0) {
            $('#listaErros').empty();
            for (var i = 0; i < errors.length; i++) {
                $('#listaErros').append('<li>' + errors[i] + '</li>');
            }
            $('#alertaErro').show();
        } else {
            // Enviar o formulário se não houver erros
            $('#criarPedidoForm').submit();
        }
    });
});

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

document.getElementById('addProdutoBtn').addEventListener('click', function() {
    var produtosDiv = document.getElementById('produtos');
    var novoProduto = produtosDiv.cloneNode(true); // Clona o bloco de produto
    novoProduto.querySelectorAll('input').forEach(function(input) {
        input.value = ''; // Limpa os valores dos inputs
    });
    produtosDiv.parentNode.insertBefore(novoProduto, this); // Insere antes do botão
});

// Função para calcular o valor total
function calcularValorTotal() {
    let total = 0;
    
    // Itera sobre todos os produtos
    document.querySelectorAll('#produtos').forEach(function(produtoDiv) {
        let quantidade = produtoDiv.querySelector('input[name="quantidade[]"]').value;
        let valorUnitario = produtoDiv.querySelector('input[name="valor_unitario[]"]').value;
        
        // Calcula o total de cada produto e adiciona ao valor total
        if (quantidade && valorUnitario) {
            total += parseFloat(quantidade) * parseFloat(valorUnitario);
        }
    });

    // Atualiza o campo de valor total
    document.getElementById('valor_total').value = total.toFixed(2);
}

// Adiciona o evento de cálculo ao mudar quantidade ou valor unitário
document.addEventListener('input', function(event) {
    if (event.target.name === 'quantidade[]' || event.target.name === 'valor_unitario[]') {
        calcularValorTotal();
    }
});
// Adicionar valor unitario 
document.addEventListener('DOMContentLoaded', function() {
    const produtoSelect = document.querySelector('#id_produto');
    const valorUnitarioInput = document.querySelector('#valor_unitario');
    
    produtoSelect.addEventListener('change', function() {
        const selectedOption = produtoSelect.options[produtoSelect.selectedIndex];
        const valor = selectedOption.getAttribute('data-valor');
        valorUnitarioInput.value = valor || '';
    });
});