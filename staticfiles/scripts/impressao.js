function exibirDataAtual() {
    // Criar um novo objeto Date (que representa a data e hora atuais)
    var dataAtual = new Date();

    // Obter o dia, mês e ano da data atual
    var dia = ("0" + dataAtual.getDate()).slice(-2);
    var mes = ("0" + (dataAtual.getMonth() + 1)).slice(-2); // O mês é baseado em zero (janeiro = 0), então adicionamos 1
    var ano = dataAtual.getFullYear();

    // Formatar a data como "DD/MM/AAAA" (por exemplo, "14/04/2024")
    var dataFormatada = dia + '/' + mes + '/' + ano;

    // Obter o elemento HTML onde queremos exibir a data atual
    var elementoDataAtual = document.getElementById('dataAtual');

    // Atualizar o conteúdo do elemento com a data formatada
    elementoDataAtual.textContent = "Data de Hoje: " + dataFormatada;
}

// Chamar a função para exibir a data atual quando a página terminar de carregar
window.onload = exibirDataAtual;

