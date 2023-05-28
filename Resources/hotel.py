from flask_restful import Resource, reqparse
from models.hotel import HotelModel
from flask_jwt_extended import jwt_required
import sqlite3
from Resources.filtros import consulta_sem_cidade, consulta_com_cidade, normalize_path_params
from models.site import SiteModel


# path /hoteis?cidade=Rio de Janeiro&estrelas_min=4&diaria_max=400
path_params = reqparse.RequestParser()
path_params.add_argument('cidade', type=str, location='args')
path_params.add_argument('estrelas_min', type=float, location='args')
path_params.add_argument('estrelas_max', type=float, location='args')
path_params.add_argument('diaria_min', type=float, location='args')
path_params.add_argument('diaria_max', type=float, location='args')
path_params.add_argument('limit', type=float, location='args')
path_params.add_argument('offset', type=float, location='args')


# Define uma classe Hoteis que herda da classe Resource
class Hoteis(Resource):
    # Método GET para a classe Hoteis

    def get(self):
        connection = sqlite3.connect('instance/banco.db')
        cursor = connection.cursor()

        dados = path_params.parse_args()
        dados_validos = {chave: dados[chave]
                         for chave in dados if dados[chave] is not None}
        parametros = normalize_path_params(**dados_validos)

        if not parametros.get('cidade'):
            tupla = tuple([parametros[chave] for chave in parametros])
            resultado = cursor.execute(consulta_sem_cidade, tupla)
        else:
            tupla = tuple([parametros[chave] for chave in parametros])
            resultado = cursor.execute(consulta_com_cidade, tupla)

        hoteis = []
        for linha in resultado:
            hoteis.append({
                'hotel_id': linha[0],
                'nome': linha[1],
                'estrelas': linha[2],
                'diaria': linha[3],
                'cidade': linha[4],
                'site_id': linha[5]
            })

        return {'hoteis': hoteis}  # SELECT * FROM hoteis


class Hotel(Resource):
    # validar os atributoss passados nas solicitações HTTP.
    atributos = reqparse.RequestParser()
    atributos.add_argument('nome', type=str, required=True,
                           help="The field 'nome' cannot be left blank")
    atributos.add_argument('estrelas', type=float, required=True,
                           help="he field 'estrelas' cannot be left blank")
    atributos.add_argument('diaria', required=True)
    atributos.add_argument('cidade')
    atributos.add_argument('site_id', type=int, required=True,
                           help="every hotel needs to be linked with a site")

    def get(self, hotel_id):
        hotel = HotelModel.find_hotel(hotel_id)
        if hotel:
            return hotel.json()
        return {'message': 'Hotel not found'}, 404  # not found.

    @jwt_required()
    def post(self, hotel_id):
        if HotelModel.find_hotel(hotel_id):

            # Bad Request
            return {"message": "Hotel id {} already exists".format(hotel_id)}, 400

        # Analisa os atributoss da requisição usando o RequestParser.
        dados = Hotel.atributos.parse_args()
        hotel = HotelModel(hotel_id, **dados)

        if not SiteModel.find_by_id(dados['site_id']):
            return {'message': 'The hotel must be associated to a valid site d.'}, 400

        try:
            hotel.save_hotel()
        except:
            # Server error
            return {'message': 'An internal error ocurred trying save hotel'}, 500
        return hotel.json()

    @jwt_required()
    def put(self, hotel_id):
        dados = Hotel.atributos.parse_args()
        hotel_found = HotelModel.find_hotel(hotel_id)
        if hotel_found:
            # Atualiza as informações do hotel com os novos dados.
            hotel_found.update_hotel(**dados)
            hotel_found.save_hotel()
            return hotel_found.json(), 200  # ok
        hotel = HotelModel(hotel_id, **dados)
        try:
            hotel.save_hotel()
        except:
            # Server error
            return {'message': 'An internal error ocurred trying save hotel'}, 500
        return hotel.json(), 201  # created

    @jwt_required()
    def delete(self, hotel_id):
        hotel = HotelModel.find_hotel(hotel_id)
        if hotel:
            try:
                hotel.delete_hotel()
            except:
                # Server error
                return {'message': 'An internal error ocurred trying save hotel'}, 500
            return {'message': 'Hotel deleted'}
        return {'message': 'Hotel not found'}
