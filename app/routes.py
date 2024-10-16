from app import app
from flask import render_template, request, redirect, url_for
import requests
import json

link = "https://flasktinterick-default-rtdb.firebaseio.com/"

@app.route('/')
@app.route('/index')
def index():
    return render_template('index.html', titulo="")

@app.route('/contato')
def contato():
    return render_template('contato.html', titulo="Consultar CPF")

@app.route('/cadastro')
def cadastro():
    return render_template('cadastro.html', titulo="Cadastrar CPF")

@app.route('/cadastrarUsuario', methods=['POST'])
def cadastrarUsuario():
    try:
        cpf = request.form.get("cpf")
        nome = request.form.get("nome")
        telefone = request.form.get("telefone")
        endereco = request.form.get("endereco")
        dados = {"cpf": cpf, "nome": nome, "telefone": telefone, "endereco": endereco}
        requisicao = requests.post(f'{link}/cadastro.json', data=json.dumps(dados))
        if requisicao.status_code == 200:
            return redirect(url_for('index'))
        else:
            return 'Erro ao cadastrar usuário.', 500
    except Exception as e:
        return f'Ocorreu um erro: {e}', 500

@app.route('/listar')
def listarTudo():
    try:
        requisicao = requests.get(f'{link}/cadastro.json')
        dicionario = requisicao.json()
        return render_template('listar.html', cadastros=dicionario)
    except Exception as e:
        return f'Algo deu errado: {e}', 500

@app.route('/listarIndividual/<cpf>')
def listarIndividual(cpf):
    try:
        requisicao = requests.get(f'{link}/cadastro.json')
        dicionario = requisicao.json()
        for codigo, dados in dicionario.items():
            if dados['cpf'] == cpf:
                return render_template('listar_individual.html', cadastro=dados)
        return 'CPF não encontrado.', 404
    except Exception as e:
        return f'Algo deu errado: {e}', 500

@app.route('/atualizar/<id>', methods=['POST'])
def atualizar(id):
    try:
        nome = request.form.get("nome")
        dados = {"nome": nome}
        requisicao = requests.patch(f'{link}/cadastro/{id}.json', data=json.dumps(dados))
        if requisicao.status_code == 200:
            return "Atualizado com sucesso!"
        else:
            return 'Erro ao atualizar.', 500
    except Exception as e:
        return f'Algo deu errado: {e}', 500

@app.route('/excluir/<id>', methods=['POST'])
def excluir(id):
    try:
        requisicao = requests.delete(f'{link}/cadastro/{id}.json')
        if requisicao.status_code == 200:
            return "Excluído com sucesso!"
        else:
            return 'Erro ao excluir.', 500
    except Exception as e:
        return f'Algo deu errado: {e}', 500
