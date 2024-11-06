from flask import render_template, request, redirect, session, flash, url_for, Blueprint
from jogoteca import app
from models import Usuarios
from helpers import *
from flask_bcrypt import check_password_hash

user_blueprint = Blueprint('user', __name__)

@app.route('/login' )
def login():
    proxima = request.args.get('proxima')
    form = FormularioUsuario()
    return render_template('login.html', titulo='Faça seu login', proxima=proxima, form=form)

@app.route('/autenticar', methods=['POST',])
def autenticar():
    form = FormularioUsuario(request.form)
    usuario = Usuarios.query.filter_by(nickname=form.nickname.data).first()
    senha = check_password_hash(usuario.senha, form.senha.data)
    if usuario and senha: #==True
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
