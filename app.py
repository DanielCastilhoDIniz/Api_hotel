from flask import Flask, jsonify
from flask_restful import Resource, Api
from Resources.hotel import Hoteis, Hotel
from Resources.usuario import User, UserRegister, UserLogin, UserLogout
from flask_jwt_extended import JWTManager
from blacklist import BLACKLIST


"""
# instanciar a classe FLask
O objeto app é uma instância da classe Flask e representa sua aplicação Flask. 
Ele será usado para configurar e definir as rotas, bem como para lidar com solicitações HTTP.
"""
app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///banco.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['JWT_SECRET_KEY'] = "ksjfksfsgfsgffdskfgs"
app.config['JWT_BLACKLIST_ENABLED'] = True
api = Api(app)
jwt = JWTManager(app)


@app.before_first_request
def cria_banco():
    banco.create_all()


@jwt.token_in_blocklist_loader
def verifica_blacklist(self, token):
    return token['jti'] in BLACKLIST


@jwt.revoked_token_loader
def token_de_acesso_invalidado(jwt_header, jwt_payload):
    # unauthorized
    return jsonify({'message': 'you have been logged out.'}), 401


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
api.add_resource(UserLogin, '/login')
api.add_resource(UserLogout, '/logout')


if __name__ == '__main__':
    from sql_alchemy import banco
    banco.init_app(app)
    app.run(debug=True)
