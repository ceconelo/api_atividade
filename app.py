from flask import Flask, request
from flask_restful import Resource, Api
from models import Pessoas, Atividades
import json

app = Flask(__name__)
api = Api(app)

class Pessoa(Resource):
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


api.add_resource(Pessoa, '/pessoa/<string:nome>')
api.add_resource(ListaPessoas, '/pessoa')
api.add_resource(ListaAtividades, '/atividades')


if __name__ == '__main__':
    app.run(debug=True)