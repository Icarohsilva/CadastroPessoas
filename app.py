from flask import Flask, render_template, request, redirect, url_for, session
from flask_sqlalchemy import SQLAlchemy
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField, SubmitField, IntegerField, DateField
from wtforms.validators import InputRequired, Length, Email, EqualTo, ValidationError,DataRequired
from werkzeug.security import generate_password_hash
from flask_mail import Message, Mail
import random
import string
import os
import webbrowser   
from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas
from sqlalchemy import func
from io import BytesIO
import base64
import matplotlib.pyplot as plt
from forms import CadastroForm, EnderecoForm, SenhaForm  # Importe os formulários corretamente



# Configurar o Flask
app = Flask(__name__)
app.config['SECRET_KEY'] = 'your_secret_key_here'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///data.db'
app.config['MAIL_SERVER'] = 'smtp.gmail.com'
app.config['MAIL_PORT'] = 587
app.config['MAIL_USE_TLS'] = True
app.config['MAIL_USERNAME'] = 'seu_email@gmail.com'  # Substitua pelo seu email
app.config['MAIL_PASSWORD'] = 'sua_senha'  # Substitua pela sua senha

# Criar instância do Flask-Mail
mail = Mail(app)
db = SQLAlchemy(app)

# Definir as tabelas no banco de dados
class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    nome_completo = db.Column(db.String(100), nullable=False)
    idade = db.Column(db.Integer)
    genero = db.Column(db.String(10))
    endereco = db.relationship('Endereco', backref='user', uselist=False)
    email = db.Column(db.String(100), unique=True)
    telefone = db.Column(db.String(20))
    cpf = db.Column(db.String(14))
    documento = db.Column(db.String(100))
    data_nascimento = db.Column(db.Date)
    senha = db.Column(db.String(100))
    # Adicione mais campos conforme necessário

class Endereco(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    rua = db.Column(db.String(100))
    numero = db.Column(db.String(20))
    cidade = db.Column(db.String(50))
    estado = db.Column(db.String(20))
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))

# Definir os formulários
class LoginForm(FlaskForm):
    email = StringField('Email', validators=[InputRequired(), Email()])
    senha = PasswordField('Senha', validators=[InputRequired()])
    lembrar = BooleanField('Lembrar-me')
    enviar = SubmitField('Entrar')

class RecuperarSenhaForm(FlaskForm):
    email = StringField('Email', validators=[InputRequired(), Email()])
    enviar = SubmitField('Enviar')

class NovaSenhaForm(FlaskForm):
    senha = PasswordField('Nova Senha', validators=[InputRequired(), EqualTo('confirma_senha', message='Senhas devem coincidir')])
    confirma_senha = PasswordField('Confirmar Senha')
    enviar = SubmitField('Alterar Senha')

@app.route('/')
def index():
    return redirect(url_for('login'))

# Rota de login
@app.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        # Realizar verificação de login e autenticação
        # Redirecionar para a página após o login bem-sucedido
        return redirect(url_for('pagina_apos_login'))
    return render_template('login.html', form=form)

# Rota de cadastro
@app.route('/cadastro', methods=['GET', 'POST'])
def cadastro():
    form = CadastroForm()
    if form.validate_on_submit():
        # Processar dados do formulário e salvar no banco de dados
        # Redirecionar para a página de login ou outra página
        return redirect(url_for('login'))
    return render_template('cadastro.html', form=form)

# Rota para cadastro de endereço
@app.route('/cadastro/endereco', methods=['GET', 'POST'])
def endereco_cadastro():
    form = EnderecoForm()
    if form.validate_on_submit():
        # Processar e salvar os dados do formulário de endereço no banco de dados
        endereco = Endereco(rua=form.rua.data, numero=form.numero.data, cidade=form.cidade.data, estado=form.estado.data)
        db.session.add(endereco)
        db.session.commit()
        
        # Redirecionar para a próxima etapa de cadastro (por exemplo, Senha)
        return redirect(url_for('senha_cadastro'))
    return render_template('endereco_cadastro.html', form=form)

# Rota para cadastro de senha
@app.route('/cadastro/senha', methods=['GET', 'POST'])
def senha_cadastro():
    form = SenhaForm()
    if form.validate_on_submit():
        # Processar e salvar os dados do formulário de senha no banco de dados
        user_id = session.get('user_id')
        if user_id:
            user = User.query.get(user_id)
            if user:
                user.senha = generate_password_hash(form.senha.data, method='sha256')
                db.session.commit()
                return redirect(url_for('login'))

    return render_template('senha_cadastro.html', form=form)

# Rota para gerar PDF
@app.route('/gerar_pdf/<int:user_id>')
def gerar_pdf(user_id):
    user = User.query.get_or_404(user_id)

    pdf_file = f"static/pdf/{user.nome_completo}_cadastro.pdf"
    pdf_path = os.path.join(app.root_path, pdf_file)

    c = canvas.Canvas(pdf_path, pagesize=letter)
    c.drawString(100, 750, "Dados do Cadastro")
    c.drawString(100, 700, f"Nome: {user.nome_completo}")
    c.drawString(100, 675, f"Idade: {user.idade}")

    # Incluir mais campos do formulário no PDF
    c.drawString(100, 650, f"Gênero: {user.genero}")
    c.drawString(100, 625, f"Endereço: {user.endereco.rua}, {user.endereco.numero}, {user.endereco.cidade}, {user.endereco.estado}")
    c.drawString(100, 600, f"Email: {user.email}")
    c.drawString(100, 575, f"Telefone: {user.telefone}")
    c.drawString(100, 550, f"CPF: {user.cpf if user.cpf else 'N/A'}")
    c.drawString(100, 525, f"Documento: {user.documento if user.documento else 'N/A'}")
    c.drawString(100, 500, f"Data de Nascimento: {user.data_nascimento.strftime('%d/%m/%Y') if user.data_nascimento else 'N/A'}")
    
    # Salvar o PDF
    c.save()
    return redirect(url_for('index'))

@app.route('/lista_cadastros', methods=['GET', 'POST'])
def lista_cadastros():
    if 'user_id' not in session:
        return redirect(url_for('login'))

    user_id = session['user_id']
    user = User.query.get_or_404(user_id)
    if user.email != 'admin@admin.com':
        return redirect(url_for('pagina_apos_login'))

    cadastros = User.query.all()

    estados = db.session.query(User.endereco.estado, func.count(User.id)).group_by(User.endereco.estado).all()
    estados = dict(estados)
    estados = {estado: estados.get(estado, 0) for estado in ['SP', 'RJ', 'MG', 'RS', 'PR']}  # Substitua pela lista completa de UF

    if request.method == 'POST':
        filtro_estado = request.form.get('filtro_estado')
        if filtro_estado:
            cadastros = User.query.join(User.endereco).filter(Endereco.estado == filtro_estado).all()  # Correção aqui

    return render_template('lista_cadastros.html', cadastros=cadastros, estados=estados)

@app.route('/grafico', methods=['GET'])
def grafico():
    if 'user_id' not in session:
        return redirect(url_for('login'))

    user_id = session['user_id']
    user = User.query.get_or_404(user_id)
    if user.email != 'admin@admin.com':
        return redirect(url_for('pagina_apos_login'))

    estados = db.session.query(Endereco.estado, func.count(User.id)).join(User).group_by(Endereco.estado).all()  # Correção aqui
    estados = dict(estados)
    estados = {estado: estados.get(estado, 0) for estado in ['SP', 'RJ', 'MG', 'RS', 'PR']}  # Substitua pela lista completa de UF

    plt.bar(estados.keys(), estados.values())
    plt.xlabel('Estado')
    plt.ylabel('Quantidade')
    plt.title('Quantidade de Cadastros por Estado')

    img_stream = BytesIO()
    plt.savefig(img_stream, format='png')
    plt.close()

    img_stream.seek(0)
    img_data = base64.b64encode(img_stream.read()).decode()

    return render_template('grafico.html', img_data=img_data)

@app.route('/recuperar_senha', methods=['GET', 'POST'])
def recuperar_senha():
    form = RecuperarSenhaForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        if user:
            # Gerar senha temporária
            temp_password = ''.join(random.choices(string.ascii_uppercase + string.digits, k=8))
            user.senha = generate_password_hash(temp_password, method='sha256')
            db.session.commit()

            # Enviar email com a senha temporária
            msg = Message('Recuperação de Senha', sender='seu_email@gmail.com', recipients=[user.email])
            msg.body = f'Sua nova senha temporária é: {temp_password}'
            mail.send(msg)

            return redirect(url_for('login'))

    return render_template('recuperar_senha.html', form=form)


@app.route('/nova_senha', methods=['GET', 'POST'])
def nova_senha():
    form = NovaSenhaForm()
    if form.validate_on_submit():
        # Validações e atualização da senha no banco de dados
        user_id = session.get('user_id')
        if user_id:
            user = User.query.get(user_id)
            if user:
                user.senha = generate_password_hash(form.senha.data, method='sha256')
                db.session.commit()
                return redirect(url_for('login'))

    return render_template('nova_senha.html', form=form)


if __name__ == '__main__':
    with app.app_context():
        # Criação das tabelas no banco de dados
        db.create_all()

        # Criação do usuário ADMIN
        admin_user = User.query.filter_by(email='admin@admin.com').first()
        if not admin_user:
            admin_user = User(nome_completo='Admin', email='admin@admin.com', senha=generate_password_hash('admin_password', method='sha256'))
            db.session.add(admin_user)
            db.session.commit()

    # Abrir o navegador automaticamente ao iniciar o aplicativo
    webbrowser.open_new_tab('http://127.0.0.1:5000/')

    app.run(debug=True)