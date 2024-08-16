from dotenv import load_dotenv
import os

load_dotenv()

hostdbs = os.environ["host"]
dbname = os.environ["database"]
usermdb = os.environ["user"]
pwdb = os.environ["password"]
sk = os.environ["sk"]
FLASK_RUN_HOST = os.environ["FLASK_RUN_HOST"]
FLASK_RUN_PORT = os.environ["FLASK_RUN_PORT"]
appinfo = os.environ["appinfo"]
storeinfo = os.environ["storeinfo"]
creator = os.environ["creator"]
ipserver = os.environ["IPSERVER"]


DATABASE_CONEXION_URI = f'mariadb+mariadbconnector://{usermdb}:{pwdb}@{hostdbs}/{dbname}'