from flask import Flask
from flask_restful import Resource, reqparse
from models.usuario import UserModel


class User(Resource):

    # /usuarios/{user_id}
    def get(self, user_id):
        user = UserModel.find_user(user_id)
        if user:
            return user.json()
        return {'message': 'User not found'}, 404  # not found.

    def delete(self, user_id):
        user = UserModel.find_user(user_id)
        if user:
            try:
                user.delete_user()
            except:
                # Server error
                return {'message': 'An internal error ocurred trying save user'}, 500
            return {'message': 'user deleted'}
        return {'message': 'User not found'}

class UserRegister(Resource):
    # cadastro
    def post(self):
        atributos = reqparse.RequestParser()
        atributos.add_argument('login', type=str, required=True, help="te field 'login' cannot be left blanc")
        atributos.add_argument('senha', type=str, required=True, help="te field 'senha' cannot be left blanc")
        dados = atributos.parse_args()

        if UserModel.find_by_login(dados['login']):
            return {"message":" The login '{}'already exist".format(dados['login'])}
        
        user = UserModel(**dados)
        user.save_user()
        return {"message": "User created successfully"}, 201 # created