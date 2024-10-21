from app import app
from flask import render_template
from flask import request
import requests
import json
link = "https://flasktinterick-default-rtdb.firebaseio.com/"
@app.route('/')
@app.route('/index')
def index():
    return render_template('index.html')

@app.route('/contato')
def contato():
    return render_template('contato.html', titulo="Contatos")

@app.route('/cadastro')
def cadastro():
    return render_template('cadastro.html', titulo="Cadastrar")

@app.route('/cadastrarUsuario', methods=['POST'])
def cadastrarUsuario():
    try:
        cpf        = request.form.get("cpf")
        nome       = request.form.get("nome")
        telefone   = request.form.get("telefone")
        endereco   = request.form.get("endereco")
        dados      = {"cpf":cpf, "nome":nome, "telefone":telefone, "endereco":endereco}
        requisicao = requests.post(f'{link}/cadastro/.json', data = json.dumps(dados))
        return 'Cadastrado com sucesso!'
    except Exception as e:
        return f'Ocorreu um erro\n +{e}'

@app.route('/listar')
def listarTudo():
    try:
        requisicao = requests.get(f'{link}/cadastro/.json')
        dicionario = requisicao.json()
        return dicionario
    except Exception as e:
        return f'algo deu errado \n {e}'

@app.route('/listarIndividual')
def listarIndividual():


    try:
        requisicao = requests.get(f'{link}/cadastro/.json')
        dicionario = requisicao.json()
        idCadastro = ""
        for codigo in dicionario:
            chave = dicionario[codigo]['cpf']
            if chave == '12345':
                idCadastro = codigo
                return idCadastro
    except Exception as e:
        return f'Algo deu errado \n {e}'


@app.route('/atualizar')
def atualizarTudo():
    return render_template('/atualizar.html', titulo="Atualizar")


@app.route('/cadastroAtualizar', methods=['POST'])
def atualizar():
    try:
        cpf = request.form.get("cpf")
        nome = request.form.get("nome")
        telefone = request.form.get("telefone")
        endereco = request.form.get("endereco")

        dados = {"nome": nome, "telefone": telefone, "endereco": endereco}
        idCadastro = listarIndividual(cpf)
        requisicao = requests.patch(f'{link}/cadastro/{idCadastro}/.json', data=json.dumps(dados))
        return render_template('atualizar.html', titulo="Atualizar cadastro")
    except Exception as e:
        return f'Ocorreu um erro\n {e}'

@app.route('/excluir')
def excluirTudo():
    return render_template('/excluir.html', titulo="Excluir")

@app.route('/excluir')
def excluir():


    try:
        requisicao = requests.delete(f'{link}/cadastro/-O8miQL89AKNB52s1xU5/.json')
        return render_template('excluir.html', titulo="Excluir Usuário")
    except Exception as e:
        return f'Algo deu errado\n {e}'