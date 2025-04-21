let stepAtual = 0;
const steps = document.querySelectorAll(".step");

function showStep(index) {
  steps.forEach((step, i) => {
    step.style.display = i === index ? "block" : "none";
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


document.getElementById ("btn_cadastrar").addEventListener ("click", validarSenhas, false);

document.getElementById ("btn_dispose").addEventListener ("click", disposeDiv, false);
div_erro = document.getElementById("erro_div")

function validarSenhas() {
    const senha = document.getElementById("senha").value;
    const confirmar = document.getElementById("validSenha").value;
    const erro = document.getElementById("mensagemErro");

    if (senha !== confirmar) {
    erro.textContent = "As senhas não coincidem.";
      return false; // impede o envio do formulário
    }

    erro.textContent = ""; // limpa a mensagem se estiver tudo certo
    return true; // permite o envio do formulário
}

function disposeDiv(){
    div_erro.style.display = 'none';
}