from models.entities.User import User
from models.ModelUsersdb import Usuarios
from flask_login import login_user


class Authenticate():
    @classmethod
    def login(self, userdata, password):
        try:
            # consulta del usuario
            # user = User(userdata[0].id, userdata[0].username, None, userdata[0].fullname, userdata[0].rol)

            if User.check_password(userdata.password, password):
                # pasa los parametros
                user = User(userdata.id, userdata.username,
                            None, userdata.fullname, userdata.rol)
                login_user(user)
                return True
            else:
                return False
        except Exception as ex:
            raise Exception(ex)

    @classmethod
    def get_by_id(self, id):

        try:

            userdata = Usuarios.query.get(id)

            if userdata != None:
                # pasa los parametros al UserMixin
                user = User(userdata.id, userdata.username,
                            None, userdata.fullname, userdata.rol)
                return user
            else:
                return None
        except Exception as ex:
            raise Exception(ex)
