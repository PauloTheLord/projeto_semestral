const input_pesquisar = document.getElementById('pesquisar');
const consultas_geral = document.getElementById('consultas-geral');
const no_found = document.getElementById('no-found');

input_pesquisar.addEventListener('keyup', () => 
{
    let expressao = input_pesquisar.value.toLowerCase();

    /*
    if (expressao.length === 1) {
        return;
    }
    */

    let consulta_individual = consultas_geral.getElementsByClassName('consulta-individual');
    var semConsultas = true;

    console.log(consulta_individual);
    for (let posicao in consulta_individual) {
        if (true === isNaN(posicao)) {
            continue;
        }

        let conteudoDoPaciente = consulta_individual[posicao].innerHTML.toLowerCase();

        if (true === conteudoDoPaciente.includes(expressao)) {
            consulta_individual[posicao].style.display = '';
            consultas_geral.style.display = '';
            no_found.textContent = "";
        }
        else {
            consulta_individual[posicao].style.display = 'none';
        }

        for (var i = 0; i < consulta_individual.length; i++) {
            if (consulta_individual[i].style.display !== 'none') {
                semConsultas = false;
                break;
            }
        }

        if (semConsultas) {
            no_found.textContent = "Consulta não encontrada...";
            consultas_geral.style.display = 'none';
        }
    }
});