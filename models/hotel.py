from sql_alchemy import banco




class HotelModel(banco.Model):
    __table_name__ = 'hoteis'

    hotel_id = banco.Column(banco.String, primary_key=True)
    nome = banco.Column(banco.String(80))
    estrelas = banco.Column(banco.Float(precision=1))
    diarias = banco.Column(banco.Float(precision=2))
    cidade = banco.Column(banco.String(40))

    def __init__(self, hotel_id, nome, estrelas, diarias, cidade):
        self.hotel_id = hotel_id
        self.nome = nome
        self.estrelas = estrelas
        self.diarias = diarias
        self.cidade = cidade

    def json(self):
        return {
            "hotel_id": self.hotel_id,
            "nome": self.nome,
            "estrelas": self.estrelas,
            "diarias": self.diarias,
            "cidade": self.cidade
        }
