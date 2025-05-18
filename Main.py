#COMENTARIO DE TESTE
from flask  import Flask, render_template, request, redirect, flash, url_for, session
#permissão: pip install flask-sqlalchemy
from flask_sqlalchemy import SQLAlchemy
# biblioteca responsável pelo gerenciamneto do login (precisa do pip install flask-login ) 
from flask_login import LoginManager, login_user, UserMixin, login_required, logout_user, current_user
import smtplib, ssl
from random import randint  
from email.message import EmailMessage
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

smtp_sever = 'smtp.gmail.com' #email para a biblioteca smtplib funcionar 
smtp_port = 587  #porta para a biblioteca smtplib funcionar
username = 'medday004@gmail.com' #email criado para o projeto
passaword = 'iryg zmqh ztuy hkxt' #senha criada pelo opção senhas de app do google

# a linha abaixo inicia a variavel de aplicação
#Se não colocar URI não tem como conectar o banco em pg html
app = Flask(__name__)

#permite o flask_login funcionar corretamente 
app.secret_key="MedDay"

#Variável que permite o acesso ao flask_login atravéz da variável de aplicação utilizada como parâmetro 
lm = LoginManager(app)

#faz com que caso o usuário não esteja logado seja direcionado autoamticamente para login
lm.login_view = '/login'

app.config['SQLALCHEMY_DATABASE_URI']  = \
    'mysql+pymysql://root:Lucas_62@localhost:3306/projeto_semestral'

#a linha abaixo instancia o banco de dados
db = SQLAlchemy(app)

#usando o conceito de herança
class UsuarioBase(UserMixin, db.Model):
    __abstract__ = True  # Diz ao SQLAlchemy que essa classe não vira tabela
    nome = db.Column(db.String(200), nullable=False)
    senha = db.Column(db.String(200), nullable=False)
    tipo_de_usuario = db.Column(db.String(100), nullable=True)


#UserMixin permite que o flask_login reconhecer a seguinte classe de usuário
class Cadastro_paciente(UsuarioBase):
    cpf = db.Column(db.String(11), primary_key =True)
    email = db.Column(db.String(200),  nullable=False)
    data_nasc = db.Column(db.String(200),  nullable=False)
    telefone = db.Column(db.String(11), nullable=False)
    cep = db.Column(db.String(8), nullable=False)
    rua = db.Column(db.String(200), nullable=True)
    bairro = db.Column(db.String(200), nullable=True)
    cidade = db.Column(db.String(200), nullable=True)
    UF = db.Column(db.String(2), nullable=False)

    #O UserMixin por padrão espera que exista um campo chamado id para usar como identificador,
    #mas já que cpf é o indentificador é necessáio usar a seguinte função para mudar o identificador padrão 
    def get_id(self):
        return str(self.cpf)


#UserMixin permite que o flask_login reconhecer a seguinte classe de usuário
class Cadastro_adm (UsuarioBase):
    matricula = db.Column(db.String(11), primary_key =True)

    #O UserMixin por padrão espera que exista um campo chamado id para usar como identificador,
    #mas já que cpf é o indentificador é necessáio usar a seguinte função para mudar o identificador padrão 
    def get_id(self):
        return str(self.matricula)
    
class Consultas(UserMixin, db.Model):
    id_consulta = db.Column(db.Integer, primary_key=True, autoincrement=True)
    cpf_paciente = db.Column(db.String(11), nullable=False)
    data_consulta = db.Column(db.String(200),  nullable=False)
    hora_consulta = db.Column(db.String(200),  nullable=False)
    especialidade = db.Column(db.String(100),  nullable=False)
    medico_responsavel = db.Column(db.String(200),  nullable=False)

#variável que carrega o usuário atravez da sua busca do seu cpf
@lm.user_loader
def user_loader(cpf):
    usuario = db.session.query(Cadastro_paciente).filter_by(cpf = cpf).first()
    if not usuario:
        usuario = db.session.query(Cadastro_adm).filter_by(matricula = cpf).first()
    return usuario

@app.route("/cadastrar")
def cadastrar_usuario():
    return render_template("./cadastrar.html")

@app.route("/info_confirm")
def confirmar_informacao():
    return  render_template("./confirmarInfo.html")

@app.route("/info_reset")
def resetar_senha():
    return  render_template("./resetarsenha.html")

@app.route("/")
#faz com que essa rota só possa ser acessada se estiver logado
@login_required
def home():
    return render_template("./home.html", tipo=current_user.tipo_de_usuario, nome = current_user.nome, email = getattr(current_user, 'email', None), matricula=getattr(current_user, 'matricula', None))

@app.route("/carteirinha")
def card_user():
    return render_template("./carteirinha.html", nome = current_user.nome, cpf =  current_user.cpf)
@app.route('/logout')
@login_required
def logout():
    #realiza o logout do usuário
    logout_user()
    return redirect(url_for('home'))

@app.route("/add", methods = ['POST'])
def add_banco():
    nome_input = request.form['nome']
    cpf_input = request.form['cpf']
    email_input = request.form['email']
    data_input = request.form['datanasc']
    tel_input = request.form['telefone']
    senha_input = request.form['senha']
    validsenha_input = request.form['validsenha']
    cep_input = request.form['cep']
    rua_input = request.form['rua']
    bairro_input = request.form['bairro']
    cidade_input = request.form['cidade']
    estado_input = request.form['UF']
    usuario_input = request.form['tipo_de_usuario']
        
    novo_usuario = Cadastro_paciente(nome = nome_input, cpf = cpf_input, data_nasc = data_input,
            email = email_input, senha = senha_input, telefone = tel_input, cep = cep_input, rua =  rua_input,
            bairro = bairro_input, cidade = cidade_input, UF = estado_input, tipo_de_usuario = usuario_input)


    #a  linha abaixo é equivalente a um select no banco, onde na clausula where vai o cpf imputado
    user = db.session.query(Cadastro_paciente).filter_by(cpf = cpf_input ).first()
    if user:
        alert = True

        alert_txt = "Esse CPF já foi cadastrado"

        return render_template("./cadastrar.html", alert_value = alert, txt_alert = alert_txt)

    else:
        if senha_input != validsenha_input:
            alert = True
            alert_txt = "As senhas não coincidem"
        else:    
            alert = False
            alert_txt = ""
            #a linha abaixo adiciona os dados para verificação da entrada de dados
            db.session.add(novo_usuario)

            #a linha abaixo grava as alterações no banco de dados
            db.session.commit()
            return redirect('/login')
    
#rota para confirmação de email e cpf    
@app.route("/confirm_email", methods = ['POST'])
def email_confirm():

    cpf_input = request.form['cpf']
    email_input = request.form['email_user']
    #código que gera um número aleatório que servira como código de verificação
    otp = randint(10000,99999)
    
    user = db.session.query(Cadastro_paciente).filter_by(cpf = cpf_input, email = email_input).first()
    if user:
        alert = False
        alert_txt = ""
        #informação para enviar o email
        msg = MIMEMultipart()
        #assunto e email
        msg['Subject'] = "Alterar Senha"
        #email de quem vai enviar
        msg['From'] = username
        #email que recebera a mensagem
        msg['To'] = email_input
        #conteúdo do email
        body = f"O Código para alterar a senha é: {otp}"
        #configurações para enviu do email 
        msg.attach(MIMEText(body, 'plain'))
        context = ssl.create_default_context()
        with smtplib.SMTP(smtp_sever,smtp_port) as smtp:
            smtp.starttls(context=context)
            smtp.login(username,passaword)
            smtp.send_message(msg)
        return render_template('./confirmarEmail.html', otp_code = otp, cpf_user = cpf_input ,email_user = email_input, alert_value = alert, txt_alert = alert_txt )
    else:
        otp = randint(10000,99999)
        alert = True
        alert_txt = "Cpf ou Email Invalidos"
        return render_template('./confirmarInfo.html', alert_value = alert, txt_alert = alert_txt)

@app.route("/confirm_code", methods = ['POST'])
def code_confirm():
    cpf_hidden = request.form['hidden_cpf']
    email_hidden = request.form['hidden_email']
    otp = request.form['code']
    otp_input = request.form['email_code']
    
    if otp == otp_input:
        alert = False
        alert_txt = ""
        return render_template('./resetarsenha.html', cpf = cpf_hidden, alert_value = alert, txt_alert = alert_txt)
    else:
        otp = randint(10000,99999)
        msg = MIMEMultipart()
        msg['Subject'] = "Alterar Senha"
        msg['From'] = username
        msg['To'] = email_hidden
        body = f"O Código para alterar a senha é: {otp}"
        msg.attach(MIMEText(body, 'plain'))
        context = ssl.create_default_context()
        with smtplib.SMTP(smtp_sever,smtp_port) as smtp:
            smtp.starttls(context=context)
            smtp.login(username,passaword)
            smtp.send_message(msg)
        alert = True
        alert_txt = "Código errado, verifique seu email novamente"
        return render_template('./confirmarEmail.html', alert_value = alert, txt_alert = alert_txt, otp_code = otp, cpf_user = cpf_hidden ,email_user = email_hidden,)
    
@app.route("/reset_password", methods = ['POST'])
def reset_password():
    cpf_input = request.form['cpf_user']
    senha_input = request.form['new_password']
    confirm_senha_input = request.form['new_password_confirme']
    user = db.session.query(Cadastro_paciente).filter_by(cpf = cpf_input ).first()

    if senha_input == confirm_senha_input:
        alert = False
        alert_txt = '' 
        user.senha = confirm_senha_input
        #a linha abaixo grava as alterações no banco de dados
        db.session.commit()
        return redirect("./login")
    else:
        alert = True
        alert_txt = 'As senhas não são iguas'           
    return render_template("./resetarsenha.html",cpf = cpf_input, alert_value = alert, txt_alert = alert_txt)

@app.route("/login", methods = ['GET','POST'])
def logar():
    #se o método da requisição for GET: 
    if request.method == 'GET':
        return render_template('./login.html')
    #se o método da requisição for POST: 
    elif request.method == 'POST':
        cpf_input = request.form['cpf']
        senha_input = request.form['senha']
        user = db.session.query(Cadastro_paciente).filter_by(cpf = cpf_input, senha = senha_input).first()
        if not user:
            alert = False
            alert_txt = '' 
            user = db.session.query(Cadastro_adm).filter_by(matricula = cpf_input, senha = senha_input).first()

        if not user:
            alert = True
            alert_txt = 'Usuário não encontrado' 
            return render_template("./login.html",alert_value = alert, txt_alert = alert_txt )
        else:
            alert = False
            alert_txt = '' 
            #realiza o login do usuário
            login_user(user)
            #redireciona para home depois do login
            return redirect(url_for('home')) 
        
@app.route('/agendar_consulta')
@login_required
def agendar_consulta():
    return render_template('./agendar_consulta.html')

@app.route('/agendar_banco', methods= ['POST'])
@login_required
def agendar_banco():
    
    cpf_paciente = current_user.get_id()
    data_consulta = request.form['data']
    hora_consulta = request.form['hora']
    especialidade = request.form['especialidade']
    medico = request.form['medico']
    nova_consulta = Consultas(cpf_paciente = cpf_paciente, data_consulta=data_consulta, 
                            hora_consulta=hora_consulta, especialidade=especialidade, 
                            medico_responsavel=medico )
    db.session.add(nova_consulta)

            #a linha abaixo grava as alterações no banco de dados
    db.session.commit()
    return redirect(url_for('meus_agendamentos'))


@app.route ('/lista_agendamento')
@login_required
def meus_agendamentos():
    cpf_logado = current_user.get_id()
    agendamentos = Consultas.query.filter_by(cpf_paciente=cpf_logado).order_by(Consultas.data_consulta).all()
    return render_template('./meus_agendamentos.html', agendamentos = agendamentos)

@app.route('/editar_consulta/<int:id_consulta>')
@login_required
def editar_consulta(id_consulta):

    consulta_selecionada = Consultas.query.filter_by(id_consulta = id_consulta).first()

    return render_template('./editar_consulta.html', consulta_selecionada = consulta_selecionada)


@app.route('/reagendar_banco', methods = ['POST'])
@login_required
def reagendar_banco():

    consulta_reagendada = Consultas.query.filter_by(id_consulta = request.form['txtId']).first()
    
    consulta_reagendada.data_consulta = request.form['txtData']
    consulta_reagendada.hora_consulta = request.form['txtHora']

    db.session.add(consulta_reagendada)
    db.session.commit()

    return redirect('/lista_agendamento')

@app.route('/excluir_consulta/<int:id_consulta>')
@login_required
def excluir_consulta(id_consulta):
    Consultas.query.filter_by(id_consulta=id_consulta).delete()
    db.session.commit()
    return redirect('/lista_agendamento')


app.run(debug=True)