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
    form = FormularioJogo()
    return render_template('novo_jogo.html', titulo='Novo Jogo', form=form)

@app.route('/criar', methods=['POST',])
def criar():
    form = FormularioJogo(request.form)

    if form.validate_on_submit():
        return redirect(url_for('adicionar_jogo'))

    nome, categoria, console = formulario_valores(form)
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

    form = FormularioJogo()
    preencher_formulario(jogo, form)

    capa_jogo = recupera_imagem(id)

    return render_template('editar_jogo.html', titulo='Editar Jogo', id=id, capa_jogo=capa_jogo, form=form)

@app.route('/atualizar', methods=['POST', ])
def atualizar():
    form = FormularioJogo(request.form)
    if form.validate_on_submit():
        jogo = Jogos.query.filter_by(id=request.form['id']).first()
        jogo.nome, jogo.categoria, jogo.console = formulario_valores(form)
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
    form = FormularioUsuario()
    return render_template('login.html', titulo='Faça seu login', proxima=proxima, form=form)

@app.route('/autenticar', methods=['POST',])
def autenticar():
    form = FormularioUsuario(request.form)
    usuario = Usuarios.query.filter_by(nickname=form.nickname.data).first()
    if usuario: #==True
        if form.senha.data == usuario.senha:
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


