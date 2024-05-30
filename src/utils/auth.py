from models.entities import User


class Authenticate():
    @classmethod
    def login(self, user):
        try:
            # consulta del usuario
            consulta = "Jorge"
            if consulta != None:
                # pasa los parametros
                if user == "Jorge":
                    return True
            else:
                return None
        except Exception as ex:
            raise Exception(ex)

    @classmethod
    def get_by_id(self, db, user):

        try:
            consulta = "consulta"

            if consulta != None:
                # pasa los parametros al UserMixin

                return
            else:
                return None
        except Exception as ex:
            raise Exception(ex)
