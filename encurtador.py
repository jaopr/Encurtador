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

        @app.route('/<short_url)') # Criando uma rota do Flask utilizando a função short_url
        def redirect_to_url(short_url): # A função é chamada quando alguém acessa a rota
            url = URL.query.filter_by(short_url = short_url).first_or_404() # Inicia uma consulta na tabela URL, filtra os resultados do campo short_url e executa a consulta, retornando ou o primeiro resultado encontrado ou o erro 404
            return redirect(url.original_url)

        @app.route('/shorten', methods=['POST']) #Define a rota short, só podendo ser acessado pelo método HTTP POST, ou seja, só aceitará solicitações enviadas pelo servidor.
        def shorten_url():
            original_url = request.form['original_url'] #recebe a solicitação HTTP
            short_url = generate_short_url() # Chama a função generate_short_url para gerar uma url única.
            new_url = URL(original_url = original_url, short_url = short_url) # Cria um novo objeto URL. a orignal_url é recebida no formulário e o short_url gera uma nova e aleatória.
            db.session.add(new_url) #prepara a inserção do objeto no BD
            db.session.commit() #Commita a alteração
            return f'Shortened URL is: {short_url}' #Retorna a url gerada


