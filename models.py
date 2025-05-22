from flask_login import UserMixin
from db import db


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
