from flask import Flask
from flask_restful import Resource, reqparse
from models.usuario import UserModel
from flask_jwt_extended import create_access_token, jwt_required, get_jwt
from passlib.hash import pbkdf2_sha256, bcrypt
from blacklist import BLACKLIST


import jwt


atributos = reqparse.RequestParser()
atributos.add_argument('login', type=str, required=True,
                       help="te field 'login' cannot be left blanc")
atributos.add_argument('senha', type=str, required=True,
                       help="te field 'senha' cannot be left blanc")
atributos.add_argument('ativado', type=bool)


class User(Resource):

    # /usuarios/{user_id}
    def get(self, user_id):
        user = UserModel.find_user(user_id)
        if user:
            return user.json()
        return {'message': 'User not found'}, 404  # not found.

    @jwt_required()
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
        dados = atributos.parse_args()

        if UserModel.find_by_login(dados['login']):

            return {"message": " The login '{}'already exist".format(dados['login'])}, 400 # Bad request

        user = UserModel(**dados)
        user.ativado = False
        user.save_user()
        return {"message": "User created successfully"}, 201  # created


class UserLogin(Resource):

    @classmethod
    def post(cls):
        dados = atributos.parse_args()
        # validação e autenticação frágil, estudar como tornar senhas mais seguras e tokens do limite de tempo.
        user = UserModel.find_by_login(dados['login'])
        if user and (dados['senha'] == user.senha):
            if user.ativado:
                token_de_acesso = create_access_token({"identify": user.user_id})
                return {'access_token': token_de_acesso}, 200
            return {'message': 'User not confirmed.'}, 400
        # Unauthorized
        return {'message': 'The username or password is incorrect'}, 401
    
class UserLogout(Resource):
        @jwt_required()
        def post(self):
            jwt_id = get_jwt()['jti'] # JWT Token Identifier
            BLACKLIST.add(jwt_id)
            return {'message':'Logged out successfully'},200

class UserConfirm(Resource):
    # /conifimacao/{user_id}
    @classmethod
    def get(cls,user_id):
        user = UserModel.find_user(user_id)
        if not user:
            return {"message":"User id '{} not found.".format(user_id)}, 404
        
        user.ativado = True
        user.save_user()
        return{"message": "User id '{}' confirmed successfully.".format(user_id)}, 200