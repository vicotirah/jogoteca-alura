from flask import request, redirect, session, url_for
from jogoteca import app, db
import os, time 


def formulario_valores():
    return (
    request.form['nome'],
    request.form['categoria'],
    request.form['console']
    )

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

