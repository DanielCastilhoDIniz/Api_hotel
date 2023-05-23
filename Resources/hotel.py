from flask import Flask
from flask_restful import Resource, reqparse
from models.hotel import HotelModel


hoteis = [
    {
        "hotel_id": "123",
        "nome": "Hotel A",
        "estrelas": 4,
        "diarias": 150.00,
        "cidade": "São Paulo"
    },
    {
        "hotel_id": "2",
        "nome": "Hotel B",
        "estrelas": 3,
        "diarias": 120.00,
        "cidade": "Rio de Janeiro"
    },
    {
        "hotel_id": "3",
        "nome": "Hotel C",
        "estrelas": 5,
        "diarias": 200.00,
        "cidade": "Belo Horizonte"
    },
    {
        "hotel_id": "4",
        "nome": "Hotel D",
        "estrelas": 4,
        "diarias": 180.00,
        "cidade": "Salvador"
    },
    {
        "hotel_id": "5",
        "nome": "Hotel E",
        "estrelas": 2,
        "diarias": 80.00,
        "cidade": "Fortaleza"
    },
    {
        "hotel_id": "6",
        "nome": "Hotel F",
        "estrelas": 3,
        "diarias": 100.00,
        "cidade": "Porto Alegre"
    }
]


# Define uma classe Hoteis que herda da classe Resource


class Hoteis(Resource):

    # Método GET para a classe Hoteis
    def get(self):
        return {'hoteis': [hotel.json() for hotel in HotelModel.query.all()]}


class Hotel(Resource):
    # validar os argumentos passados nas solicitações HTTP.
    argumento = reqparse.RequestParser()
    argumento.add_argument('nome', type=str, required=True, help="The field 'nome' cannot be left blank")
    argumento.add_argument('estrelas', type=float, required=True, help="he field 'estrelas' cannot be left blank")
    argumento.add_argument('diarias')
    argumento.add_argument('cidade')

    def get(self, hotel_id):
        hotel = HotelModel.find_hotel(hotel_id)
        if hotel:
            return hotel.json()
        return {'message': 'Hotel not found'}, 404  # not found.

    def post(self, hotel_id):
        if HotelModel.find_hotel(hotel_id):
            # bad request
            return {"message": "Hotel id {} already exists".format(hotel_id)}, 400 #Bad Request

        # Analisa os argumentos da requisição usando o RequestParser.
        dados = Hotel.argumento.parse_args()
        hotel = HotelModel(hotel_id, **dados)
        try:
            hotel.save_hotel()
        except:
            return {'message': 'An internal error ocurred trying save hotel'}, 500 #Server error
        return hotel.json()

    def put(self, hotel_id):
        dados = Hotel.argumento.parse_args()

        # hotel = {"hotel_id": hotel_id, **dados}
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
            return {'message': 'An internal error ocurred trying save hotel'}, 500 #Server error
        return hotel.json(), 201  # created

    def delete(self, hotel_id):
        hotel = HotelModel.find_hotel(hotel_id)
        if hotel:
            try:
                hotel.delete_hotel()
            except:
                return {'message': 'An internal error ocurred trying save hotel'}, 500 #Server error
            return {'message': 'Hotel deleted'}
        return {'message': 'Hotel not found'}
