const input_pesquisar = document.getElementById('pesquisar');
const pacientes_geral = document.getElementById('pacientes-geral');
const no_found = document.getElementById('no-found');

input_pesquisar.addEventListener('keyup', () => 
{
    let expressao = input_pesquisar.value.toLowerCase();

    /*
    if (expressao.length === 1) {
        return;
    }
    */

    let paciente_individual = pacientes_geral.getElementsByClassName('paciente-individual');
    var semPacientes = true;

    console.log(paciente_individual);
    for (let posicao in paciente_individual) {
        if (true === isNaN(posicao)) {
            continue;
        }

        let conteudoDoPaciente = paciente_individual[posicao].innerHTML.toLowerCase();

        if (true === conteudoDoPaciente.includes(expressao)) {
            paciente_individual[posicao].style.display = '';
            pacientes_geral.style.display = '';
            no_found.textContent = "";
        }
        else {
            paciente_individual[posicao].style.display = 'none';
            pacientes_geral.style.display = 'none';
        }

        for (var i = 0; i < paciente_individual.length; i++) {
            if (paciente_individual[i].style.display !== 'none') {
                semPacientes = false;
                break;
            }
        }

        if (semPacientes) {
            no_found.textContent = "Paciente não encontrado...";
        }
    }
});