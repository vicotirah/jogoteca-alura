from flask import Flask
from flask_sqlalchemy import SQLAlchemy


app = Flask(__name__)
app.secret_key = 'jogoteca'

app.config.from_pyfile('config.py')

db = SQLAlchemy(app)

from views import *

if __name__ == '__main__':
    app.run(debug=True)