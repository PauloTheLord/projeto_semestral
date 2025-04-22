// Etapas do cadastro
let stepAtual = 0;
const steps = document.querySelectorAll(".step");

function showStep(index) {
  steps.forEach((step, i) => {
    step.style.display = i === index ? "flex" : "none";
  });
}

function nextStep() {
  if (stepAtual < steps.length - 1) {
    stepAtual++;
    showStep(stepAtual);
  }
}

function prevStep() {
  if (stepAtual > 0) {
    stepAtual--;
    showStep(stepAtual);
  }
}

showStep(stepAtual);

// Preenchimento automatico do CEP (ViaCEP)

// Criando variáveis referentes aos inputs do site
const cep = document.querySelector("#cep");
const rua = document.querySelector("#rua");
const bairro = document.querySelector("#bairro");
const cidade = document.querySelector("#cidade");
const uf = document.querySelector("#UF")
const message_error_cep = document.querySelector("#message_error_cep")

// Função executada sempre que o usuário desfocar do campo do CEP
cep.addEventListener('focusout', async () => {

  try {
    // Atribuindo a variáveis verificações de validação do CEP
    const onlyNumbers = /^[0-9]+$/;
    const cepValid = /^[0-9]{8}$/;

    // Caso o CEP não seja válido
    if(!onlyNumbers.test(cep.value) || !cepValid.test(cep.value)) {
      throw {cep_error: 'CEP Inválido' };
    }

    // puxando o JSON que o ViaCEP disponibiliza com base no CEP que o usuário digitar
    const response = await fetch(`https://viacep.com.br/ws/${cep.value}/json/`);

    if(!response.ok) {
      throw await response.json();
    }

    // Atribuindo a variável 'responseCep' as informações do arquivo JSON
    const responseCep = await response.json();

    // Colocando os dados do endereço nos inputs
    rua.value = responseCep.logradouro;
    bairro.value = responseCep.bairro;
    cidade.value = responseCep.localidade;
    uf.value = responseCep.uf;

  } catch (error) { // Caso o bloco de código acima apresente erro, ele apresenta a mensagem de erro no span(html)
    if(error?.cep_error) {
      message_error_cep.textContent = error.cep_error;
      setTimeout(() => {
        message_error_cep.textContent = '';
      }, 5000);
    }
  }
});

// Validação das senhas

document.getElementById ("btn_dispose").addEventListener ("click", disposeDiv, false);
div_erro = document.getElementById("erro_div")

function disposeDiv(){
    div_erro.style.display = 'none';
}