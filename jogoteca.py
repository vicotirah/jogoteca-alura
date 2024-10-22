from flask import Flask, render_template, request  # type: ignore

class Jogo:
    def __init__(self, nome, categoria, console):
        self._nome = nome
        self._categoria = categoria
        self._console = console




jogo1 = Jogo('Tetris', 'Puzzle', 'Atari')
jogo2 = Jogo('God of War', 'Aventura', 'PS2')
jogo3 = Jogo('Mortal Kombat', 'Luta', 'PS2')
lista = [jogo1, jogo2, jogo3]




app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html', titulo='Jogos', jogos = lista)

@app.route('/novo')
def adicionar_jogo():
    return render_template('novo_jogo.html', titulo='Novo Jogo')

@app.route('/criar', methods=['POST',])
def criar():
    nome =request.form['nome']
    categoria =request.form['categoria']
    console = request.form['console']
    jogo = Jogo(nome, categoria, console)
    lista.append(jogo)
    return render_template('index.html', titulo='Jogos', jogos = lista)

app.run(debug=True)