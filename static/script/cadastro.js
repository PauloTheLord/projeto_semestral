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

const cep = document.querySelector("#cep");
const rua = document.querySelector("#rua");
const bairro = document.querySelector("#bairro");
const cidade = document.querySelector("#cidade");
const message_error_cep = document.querySelector("#message_error_cep")

cep.addEventListener('focusout', async () => {

  try {
    const onlyNumbers = /^[0-9]+$/;
    const cepValid = /^[0-9]{8}$/;

    if(!onlyNumbers.test(cep.value) || !cepValid.test(cep.value)) {
      throw {cep_error: 'Cep invalid' };
    }

    const response = await fetch(`https://viacep.com.br/ws/${cep.value}/json/`);

    if(!response.ok) {
      throw await response.json();
    }

    const responseCep = await response.json();

    rua.value = responseCep.logradouro;
    bairro.value = responseCep.bairro;
    cidade.value = responseCep.localidade;

  } catch (error) {
    if(error?.cep_error) {
      message_error_cep.textContent = error.cep_error;
      setTimeout(() => {
        message_error_cep.textContent = '';
      }, 5000);
    }
    console.log(error)
  }
});

// Validação das senhas

document.getElementById ("btn_dispose").addEventListener ("click", disposeDiv, false);
div_erro = document.getElementById("erro_div")

function disposeDiv(){
    div_erro.style.display = 'none';
}