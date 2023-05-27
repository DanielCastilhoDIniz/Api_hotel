from flask import Flask
from flask_restful import Resource, reqparse
from models.hotel import HotelModel
from flask_jwt_extended import jwt_required
import sqlite3


def normalize_path_params(cidade=None,
                          estrelas_min=0,
                          estrelas_max=5,
                          diaria_min=0,
                          diaria_max=100000,
                          limit=50,
                          offset=0, **dados):
    if cidade:
        return {
            'estrelas_min': estrelas_min,
            'estrelas_max': estrelas_max,
            'diaria_min': diaria_min,
            'diaria_max': diaria_max,
            'cidade': cidade,
            'limit': limit,
            'offset': offset
        }
    return {
        'estrelas_min': estrelas_min,
        'estrelas_max': estrelas_max,
        'diaria_min': diaria_min,
        'diaria_max': diaria_max,
        'limit': limit,
        'offset': offset
    }


# path /hoteis?cidade=Rio de Janeiro&estrelas_min=4&diaria_max=400
path_params = reqparse.RequestParser()
path_params.add_argument('cidade', type=str)
path_params.add_argument('estrelas_min', type=float)
path_params.add_argument('estrelas_max', type=float)
path_params.add_argument('diaria_min', type=float)
path_params.add_argument('diaria_max', type=float)
path_params.add_argument('limit', type=float)
path_params.add_argument('offset', type=float)


# Define uma classe Hoteis que herda da classe Resource
class Hoteis(Resource):
    # Método GET para a classe Hoteis

    def get(self):
        dados = path_params.parse_args()
        dados_validos = {chave: dados['chave']
                         for chave in dados if dados['chave'] is not None}
        return {'hoteis': [hotel.json() for hotel in HotelModel.query.all()]}


class Hotel(Resource):
    # validar os argumentos passados nas solicitações HTTP.
    argumento = reqparse.RequestParser()
    argumento.add_argument('nome', type=str, required=True,
                           help="The field 'nome' cannot be left blank")
    argumento.add_argument('estrelas', type=float, required=True,
                           help="he field 'estrelas' cannot be left blank")
    argumento.add_argument('diarias')
    argumento.add_argument('cidade')

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

        # Analisa os argumentos da requisição usando o RequestParser.
        dados = Hotel.argumento.parse_args()
        hotel = HotelModel(hotel_id, **dados)
        try:
            hotel.save_hotel()
        except:
            # Server error
            return {'message': 'An internal error ocurred trying save hotel'}, 500
        return hotel.json()

    @jwt_required()
    def put(self, hotel_id):
        dados = Hotel.argumento.parse_args()
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
