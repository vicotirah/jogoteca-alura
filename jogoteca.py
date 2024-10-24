from flask import Flask, render_template, request, redirect, session, flash, url_for  # type: ignore
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.secret_key = 'jogoteca'

app.config['SQLALCHEMY_DATABASE_URI'] = \
    '{SGBD}://{usuario}:{senha}@{servidor}/{database}'.format(
    SGBD = 'mysql+mysqlconnector',
    usuario = 'root',
    senha = 'admin',
    servidor = '127.0.0.1',
    database = 'jogoteca'
    )

db = SQLAlchemy(app)


class Jogos(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    nome = db.Column(db.String(50), nullable=False)
    categoria = db.Column(db.String(40), nullable=False)
    console = db.Column(db.String(20), nullable=False)
    def __repr__(self):
        return f'<Jogo {self.nome}>'

class Usuarios(db.Model):
    nickname = db.Column(db.String(8), primary_key=True)
    nome = db.Column(db.String(20), nullable=False)
    senha = db.Column(db.String(100), nullable=False)
    def __repr__(self):
        return f'<Usuário {self.nome}>'
    
# Usando o contexto da aplicação
with app.app_context():
    try:
        db.create_all()  # Cria todas as tabelas definidas no modelo
        print("Conexão com o banco de dados bem-sucedida!")
    except Exception as e:
        print(f"Erro ao conectar ao banco de dados: {e}")

@app.route('/')
def index():
    lista = Jogos.query.order_by(Jogos.id)
    return render_template('index.html', titulo='Jogos', jogos=lista)

@app.route('/novo')
def adicionar_jogo():
    if 'usuario_logado' not in session or session['usuario_logado'] == None:
        return redirect(url_for('login', proxima=url_for('adicionar_jogo')))
    return render_template('novo_jogo.html', titulo='Novo Jogo')

@app.route('/criar', methods=['POST',])
def criar():
    nome =request.form['nome']
    categoria =request.form['categoria']
    console = request.form['console']
    
    jogo = Jogos.query.filter_by(nome=nome).first()

    if jogo: #==True
        flash('Jogo já listado!')
        return redirect(url_for('index'))

    novo_jogo = Jogos(nome=nome, categoria=categoria, console=console)
    db.session.add(novo_jogo)
    db.session.commit()

    return redirect(url_for('index'))

@app.route('/login' )
def login():
    proxima = request.args.get('proxima')
    return render_template('login.html', titulo='Faça seu login', proxima=proxima)

@app.route('/autenticar', methods=['POST',])
def autenticar():
    usuario = Usuarios.query.filter_by(nickname=request.form['usuario']).first()
    if usuario: #==True
        if request.form['senha'] == usuario.senha:
            session['usuario_logado'] = usuario.nickname
            flash(usuario.nickname + ' logado com sucesso!')
            proxima_pagina = request.form['proxima']
            return redirect(proxima_pagina)
    else:
        flash('Usuário não logado')
        return redirect(url_for('login'))
    
@app.route('/logout')
def logout():
    session['usuario_logado'] = None
    flash('Logout efetuado com sucesso') 
    return redirect(url_for('index'))

app.run(debug=True)