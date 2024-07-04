from flask import Flask, request, redirect
from flask_sqlalchemy import SQLAlchemy
import string, random

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///urls.db' #Usando o banco de dados urls do SQLite, especificado pelo URI
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False # Esse False evita que o SQLAlchemy envie notificações para o app Flask, otimizando o código
db = SQLAlchemy(app)

#Criando a classe URL
class URL(db.model): # Classe que herda o model do SQLAlchemy
    id = db.Column(db.Integer, primary_key = True) # Cria uma coluna que gera uma chave primária, sendo ela um número inteiro
    original_url = db.Column(db.String(500), nullable = False) # Recebe a URL original, com capacidade em até 500 caracteres. a opção nullable = false não permite salvar a aplicação no BD enquanto essa parte estiver em branco
    short_url = db.Column(db.String(10), unique = True, nullable = False) # Armazena a URL reduzida, com até 10 caracteres, com a função unique = true impedindo a duplicação de URLs

def generate_short_url(): #definindo a função que encurta as URLs
    characters = string.ascii_letters + string.digits # Criando um string com letras maiúsculas e minusculas e com digitos de 0 a 9
    while True: # Fica tentando criar uma URL única até conseguir
        short_url = ''.join(random.choice(characters) for _ in range(10)) # Cria um string aleatória de 10 Caracteres
        if not URL.query.filter_by(short_url=short_url).first(): #Verifica se a URL é única
            return short_url