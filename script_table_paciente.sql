create database projeto_semestral;
use projeto_semestral;


create table cadastro_paciente(
nome varchar(200) not null,
cpf char(11) primary key,
data_nasc date not null,
email varchar (100) not null,
senha varchar(200) not null,
telefone char(11) not null,
cep char(8) not null,
rua varchar(200) null,
bairro varchar(200) null,
cidade varchar(200) null,
UF char(2) not null, 
tipo_de_usuario varchar(100) not null );


create table cadastro_adm (
nome varchar(200) not null,
matricula char(11) primary key,
senha varchar(200) not null,
tipo_de_usuario varchar(100) not null );


insert into cadastro_adm 
values ('Administrador_001', '12345678911', 'admin', 'usuario_adm');

create table consultas (
id_consulta INT AUTO_INCREMENT PRIMARY KEY,
cpf_paciente char(11), 
data_consulta date,
hora_consulta varchar(100),
especialidade varchar(100),
medico_responsavel varchar(150) );






