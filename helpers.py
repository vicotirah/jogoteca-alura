from flask import request, redirect, session, url_for
from jogoteca import app, db
import os, time 
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, PasswordField, validators

class FormularioJogo(FlaskForm):
    nome = StringField('Nome do Jogo', [validators.DataRequired(), validators.Length(min=1, max=50)])
    categoria = StringField('Categoria', [validators.DataRequired(), validators.Length(min=1, max=40)])
    console = StringField('Console', [validators.DataRequired(), validators.Length(min=1, max=20)])
    salvar = SubmitField('Salvar')

class FormularioUsuario(FlaskForm):
    nickname = StringField('Nickname', [validators.DataRequired(), validators.Length(min=1, max=8)])
    senha = PasswordField('Senha', [validators.DataRequired(), validators.Length(min=1, max=100)])
    login = SubmitField('Login')

def formulario_valores(form):
    return (
    form.nome.data,
    form.categoria.data,
    form.console.data
    )

def preencher_formulario(obj, form):
    form.nome.data = obj.nome
    form.categoria.data = obj.categoria
    form.console.data = obj.console


def salvar_no_banco(objeto):
    db.session.add(objeto)
    db.session.commit()

def login_requerido(proxima_funcao):
    if 'usuario_logado' not in session or session['usuario_logado'] is None:
        return redirect(url_for('login', proxima=url_for(proxima_funcao, **request.view_args)))
    
def recupera_imagem(id):
    for nome_arquivo in os.listdir(app.config['UPLOAD_PATH']):
        if f'capa{id}' in nome_arquivo:
            return nome_arquivo
    
    return 'capa_padrao.png'

def deleta_arquivo(id):
    arquivo = recupera_imagem(id)
    if arquivo != 'capa_padrao.png':
        os.remove(os.path.join(app.config['UPLOAD_PATH'], arquivo))

def imagem_form(obj):
    arquivo = request.files['arquivo']
    if arquivo and arquivo.filename:
        deleta_arquivo(obj.id)

        upload_path = app.config['UPLOAD_PATH']
        timestamp = int(time.time())

        arquivo.save(f'{upload_path}/capa{obj.id}-{timestamp}.jpg')

        return True
    return False



