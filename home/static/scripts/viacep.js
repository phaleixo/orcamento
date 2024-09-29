/* Script para buscar endereço pelo CEP (ViaCEP)*/
document.getElementById('id_cep').addEventListener('blur', function() {
    var cep = this.value.replace(/\D/g, '');
    if (cep.length === 8) {
        fetch(`https://viacep.com.br/ws/${cep}/json/`)
        .then(response => response.json())
        .then(data => {
            if (!("erro" in data)) {
                document.getElementById('id_logradouro').value = data.logradouro;
                document.getElementById('id_bairro').value = data.bairro;
                document.getElementById('id_cidade').value = data.localidade;
                document.getElementById('id_estado').value = data.uf;
            } else {
                alert("CEP não encontrado.");
            }
        })
        .catch(error => console.error('Erro ao buscar o CEP:', error));
    }
});