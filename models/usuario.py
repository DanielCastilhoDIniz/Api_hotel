from sql_alchemy import banco
from flask import request, url_for
from requests import post


MAILGUN_DOMAIN ="sandbox42628f61c92542d2a300cf07771a270f.mailgun.org"
MAILGUN_API_KEY = "3305d42da93d1e1a0fd655998b89a353-5d9bd83c-2024718a"
FROM_TITLE ='Confirmação'
FROM_EMAIL = 'no-replay@restapihotel.com'

class UserModel(banco.Model):
    __tablename__ = 'usuarios'

    user_id = banco.Column(banco.Integer, primary_key=True)
    login = banco.Column(banco.String(40),nullable=False, unique=True)
    senha = banco.Column(banco.String(40), nullable=False)
    email = banco.Column(banco.String(90), nullable=False, unique=True)
    ativado = banco.Column(banco.Boolean, default=False  )

    def __init__(self, login, senha, email, ativado):
        self.login = login
        self.senha = senha
        self.ativado = ativado

    
    def send_confirmation_email(self):
        # http://127.0.0.1:5000/confirmacao/{user_id}'
        link = request.url_root[:-1] + url_for('userconfirm', user_id=self.user_id)

        return post('https://api.mailgun.net/v3/{}/messages'.format(MAILGUN_DOMAIN), 
                    auth=("api", MAILGUN_API_KEY),
                    data={"from": "{} <{}>".format(FROM_TITLE, FROM_EMAIL),
                          "to": self.email,
                          "subject": "Confirmação de cadastro",
                          "text": "Confirme seu cadastro clicando no link a seguir: {} ".format(link),
                          "html":"<html><p>Confirme seu cadastro clicando no link a seguir:<a href='{}'> CONFIRMAR EMAIL</a></p></html>".format(link)
                          }
                    )
          

    def json(self):
        return {
            "user_id": self.user_id,
            "login": self.login,    
            "email": self.email,    
            "ativado": self.ativado
        }

    @classmethod
    def find_user(cls, user_id):
        # SELECT * FROM hoteis WHERE user_id = $user_id
        user = cls.query.filter_by(user_id=user_id).first()
        if user:    
            return user
        return None

    @classmethod
    def find_by_login(cls, login):
        # SELECT * FROM hoteis WHERE login = $login
        user = cls.query.filter_by(login=login).first()
        if user:
            return user
        return None
    
    @classmethod
    def find_by_email(cls, email):
        # SELECT * FROM hoteis WHERE email = $email
        user = cls.query.filter_by(email=email).first()
        if user:
            return user
        return None

    def save_user(self):
        banco.session.add(self)
        banco.session.commit()

    def delete_user(self):
        banco.session.delete(self)
        banco.session.commit()
