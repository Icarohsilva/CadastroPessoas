from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, DateField
from wtforms.validators import InputRequired, Length, Email, EqualTo, ValidationError, DataRequired


class CadastroForm(FlaskForm):
    nome_completo = StringField('Nome Completo', validators=[DataRequired()])
    cpf = StringField('CPF', validators=[DataRequired()])
    email = StringField('Email', validators=[DataRequired(), Email()])
    telefone = StringField('Telefone', validators=[DataRequired()])
    data_nascimento = DateField('Data de Nascimento', validators=[DataRequired()])
    submit = SubmitField('Avançar')

class EnderecoForm(FlaskForm):
    rua = StringField('Rua', validators=[DataRequired()])
    numero = StringField('Número', validators=[DataRequired()])
    cidade = StringField('Cidade', validators=[DataRequired()])
    estado = StringField('Estado/UF', validators=[DataRequired()])
    submit = SubmitField('Avançar')


class SenhaForm(FlaskForm):
    senha = PasswordField('Nova Senha', validators=[DataRequired(), EqualTo('confirma_senha', message='Senhas devem coincidir')])
    confirma_senha = PasswordField('Confirmar Senha', validators=[DataRequired()])
    submit = SubmitField('Cadastrar')


class RecuperarSenhaForm(FlaskForm):
    email = StringField('Email', validators=[InputRequired(), Email()])
    enviar = SubmitField('Enviar')


class NovaSenhaForm(FlaskForm):
    senha = PasswordField('Nova Senha', validators=[InputRequired(), EqualTo('confirma_senha', message='Senhas devem coincidir')])
    confirma_senha = PasswordField('Confirmar Senha')
    enviar = SubmitField('Alterar Senha')
