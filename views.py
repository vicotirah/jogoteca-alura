from flask import render_template, request, redirect, session, flash, url_for, send_from_directory
from models import Jogos, Usuarios
from jogoteca import app, db
from helpers import *


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
    redirecionar = login_requerido('adicionar_jogo')
    if redirecionar:
        return redirecionar
    
    return render_template('novo_jogo.html', titulo='Novo Jogo')

@app.route('/criar', methods=['POST',])
def criar():
    nome, categoria, console = formulario_valores()
    jogo = Jogos.query.filter_by(nome=nome).first()
    if jogo: #==True
        flash('Jogo já listado!')
        return redirect(url_for('index'))
    novo_jogo = Jogos(nome=nome, categoria=categoria, console=console)

    salvar_no_banco(novo_jogo)

    imagem_form(novo_jogo)

    return redirect(url_for('index'))

@app.route('/editar/<int:id>')
def editar_jogo(id):
    redirecionar = login_requerido('editar_jogo')
    if redirecionar:
        return redirecionar
    jogo=Jogos.query.filter_by(id=id).first()

    capa_jogo = recupera_imagem(id)

    return render_template('editar_jogo.html', titulo='Editar Jogo', jogo=jogo, capa_jogo=capa_jogo)

@app.route('/atualizar', methods=['POST',])
def atualizar():
    jogo = Jogos.query.filter_by(id=request.form['id']).first()
    jogo.nome, jogo.categoria, jogo.console = formulario_valores()
    salvar_no_banco(jogo)

    imagem_form(jogo)

    return redirect(url_for('index'))

@app.route('/deletar/<int:id>')
def deletar_jogo(id):
    redirecionar = login_requerido('deletar_jogo')
    if redirecionar:
        return redirecionar
    Jogos.query.filter_by(id=id).delete()
    db.session.commit()
    flash('Jogo deletado com sucesso')

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

@app.route('/uploads/<nome_arquivo>')
def imagem(nome_arquivo):
    return  send_from_directory('uploads', nome_arquivo)


