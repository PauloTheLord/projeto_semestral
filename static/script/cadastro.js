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

