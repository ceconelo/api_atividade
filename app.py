from flask import Flask, request
from flask_restful import Resource, Api
from models import Pessoas, Atividades, Usuarios
#https://flask-httpauth.readthedocs.io/en/latest/
from flask_httpauth import HTTPBasicAuth

auth = HTTPBasicAuth()
app = Flask(__name__)
api = Api(app)

# USUARIOS = {
#     'teste':'12345'
# }
#
# @auth.verify_password
# def verificacao(login, senha):
#     if not (login, senha):
#         return False
#     return USUARIOS.get(login) == senha

@auth.verify_password
def verificacao(login, senha):
    if not (login, senha):
        return False
    return Usuarios.query.filter_by(login=login, senha=senha).first()

class ListaUsuarios(Resource):
    @auth.login_required
    def get(self):
        usuarios = Usuarios.query.all()
        response = [{'id': i.id, 'login': i.login} for i in usuarios]
        return response

    @auth.login_required
    def post(self):
        dados = request.json
        usuario = Usuarios(login=dados['login'], senha=dados['senha'])
        usuario.save()
        return {'status': 'sucesso', 'mensagem': 'O usuario {} foi inserido com sucesso.'.format(dados['login'])}

class Pessoa(Resource):
    @auth.login_required
    def get(self, nome):
        try:
            pessoa = Pessoas.query.filter_by(nome=nome).first()
            response = {
                'nome': pessoa.nome,
                'idade': pessoa.idade,
                'id': pessoa.id
            }
        except AttributeError:
            response = {
                'status':'Erro.',
                'Mensagem': 'Nome não encontrado'
            }
        return response
    def put(self, nome):
        pessoa =  Pessoas.query.filter_by(nome=nome).first()
        dados = request.json
        if  'nome' in dados:
            pessoa.nome = dados['nome']
        if 'idade' in dados:
            pessoa.idade = dados['idade']
        pessoa.save()

        response = {
            'id':pessoa.id,
            'nome':pessoa.nome,
            'idade': pessoa.idade
        }
        return response
    def delete(self, nome):
        pessoa = Pessoas.query.filter_by(nome=nome).first()
        pessoa.delete()
        response = {
            'status': 'sucesso',
            'mensagem':'Excluido com sucesso.'
        }
        return response

class ListaPessoas(Resource):
    @auth.login_required
    def get(self):
        pessoas = Pessoas.query.all()
        response = [{'id':i.id,'nome':i.nome,'idade':i.idade} for i in pessoas]
        return response

    def post(self):
        dados = request.json
        pessoa = Pessoas(nome=dados['nome'], idade=dados['idade'])
        pessoa.save()
        return {'status':'sucesso','mensagem':'O nome {} foi inserido com sucesso.'.format(dados['nome'])}

class ListaAtividades(Resource):
    @auth.login_required
    def get(self):
        atividades = Atividades.query.all()
        response = [{'nome': i.nome , 'pessoa':i.pessoa.nome, 'id': i.id} for i in atividades]
        return response

    def post(self):
        dados = request.json
        pessoa = Pessoas.query.filter_by(nome=dados['pessoa']).first()
        atividade = Atividades(nome=dados['nome'], pessoa=pessoa)
        atividade.save()
        response = {
            'pessoa':atividade.pessoa.nome,
            'nome':atividade.nome,
            'id':atividade.id
        }
        return response

api.add_resource(ListaUsuarios, '/usuario')
api.add_resource(Pessoa, '/pessoa/<string:nome>')
api.add_resource(ListaPessoas, '/pessoa')
api.add_resource(ListaAtividades, '/atividades')


if __name__ == '__main__':
    app.run(debug=True)