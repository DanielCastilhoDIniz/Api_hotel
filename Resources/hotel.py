from flask import Flask
from flask_restful import Resource, reqparse
from models.hotel import HotelModel


# Define uma classe Hoteis que herda da classe Resource
class Hoteis(Resource):

    # Método GET para a classe Hoteis
    def get(self):
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
