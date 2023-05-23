from flask import Flask
from flask_restful import Resource, Api
from Resources.hotel import Hoteis, Hotel
from Resources.usuario import User, UserRegister

"""
# instanciar a classe FLask
O objeto app é uma instância da classe Flask e representa sua aplicação Flask. 
Ele será usado para configurar e definir as rotas, bem como para lidar com solicitações HTTP.
"""
app = Flask(__name__)

"""
# cria o objeto "api"  para criação API RESTful
O objeto api é uma instância da classe Api do Flask-RESTful, que é uma extensão do Flask para criação de APIs RESTful de forma simples. A classe Api fornece recursos para criar, configurar e definir endpoints de API.

A linha api = Api(app) cria uma instância da classe Api e associa o objeto api ao aplicativo Flask app. Isso permite que você use as funcionalidades do Flask-RESTful no seu aplicativo Flask.
"""
api = Api(app)

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///banco.bd'

app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False


"""
Ao usar o decorador @app.before_first_request, você garante que a função especificada seja executada somente uma vez, no início da execução da aplicação. Isso pode ser útil para configurar o ambiente da aplicação antes de lidar com as solicitações dos usuários e garantir que tudo esteja pronto para funcionar corretamente.
"""


@app.before_first_request
def cria_banco():
    banco.create_all()


"""
# mapeando a classe Hoteis para o endpoint /hoteis da API.
Isso significa que quando uma solicitação HTTP é feita para /hoteis, o Flask-RESTful irá direcionar essa solicitação para a classe Hoteis, onde você pode definir métodos
"""
api. add_resource(Hoteis, '/hoteis')

"""
linha api.add_resource(Hotel, '/hoteis/<string:hotel_id>') está adicionando um recurso chamado Hotel à sua API Flask com um parâmetro dinâmico hotel_id na rota.

Nesse contexto, Hotel é uma classe que representa um recurso específico de hotel na sua API. Ao chamar api.add_resource(Hotel, '/hoteis/<string:hotel_id>'), você está mapeando a classe Hotel para o endpoint /hoteis/<string:hotel_id> da sua API.

Isso significa que quando uma solicitação HTTP é feita para /hoteis/<string:hotel_id>, o Flask-RESTful irá direcionar essa solicitação para a classe Hotel e passar o valor do parâmetro hotel_id como um argumento para os métodos definidos nessa classe.

Por exemplo, se você tiver o método get(hotel_id) na classe Hotel, ele será chamado quando uma solicitação GET for feita para /hoteis/<string:hotel_id>, e o valor do parâmetro hotel_id será passado como um argumento para esse método. O mesmo se aplica a outros métodos, como post(), put(), delete(), etc., que você pode definir na classe Hotel.

Essa abordagem permite criar endpoints específicos para a manipulação de um hotel individual com base no ID do hotel fornecido na URL. Por exemplo, ao fazer uma solicitação GET para /hoteis/123, o método get(123) na classe Hotel será chamado, permitindo que você obtenha as informações detalhadas do hotel com o ID 123.

Essa funcionalidade é útil quando você precisa realizar operações específicas em um único recurso em sua API.
"""
api. add_resource(Hotel, '/hoteis/<string:hotel_id>')

api.add_resource(User, '/usuarios/<int:user_id>')
api.add_resource(UserRegister, '/cadastro')


if __name__ == '__main__':
    from sql_alchemy import banco
    banco.init_app(app)
    app.run(debug=True)
