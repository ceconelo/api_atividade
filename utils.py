from models import Pessoas, db_session

#Metodo que insere uma pessoa no banco
def insere_pessoa(nome, idade):
    pessoa = Pessoas(nome=nome, idade=idade)
    pessoa.save()
#Metodo que lista todas as pessoas do banco
def listar_pessoas():
    print (Pessoas.query.all())
#Metodo que consulta pessoa pelo nome
def consulta_pessoa(nome):
    pessoa = Pessoas.query.filter_by(nome=nome).first()
    print(pessoa)
#Metodo que altera dados da pessoa
def alterar_pessoa(nome):
    pessoa = Pessoas.query.filter_by(nome=nome).first()
    pessoa.idade = 10
    pessoa.save()
#metodo que deleta a pessoa no banco
def delete_pessoa(nome):
    pessoa = Pessoas.query.filter_by(nome=nome).first()
    pessoa.delete()

if __name__ == '__main__':
    #insere('Cristina', 60)
    #consulta_nome('Jose')
    #alterar('Thiago')
    #listar_todos()
    #delete('Cristina')
    listar_pessoas()