from dotenv import load_dotenv
import os

load_dotenv()

host = os.environ["host"]
database = os.environ["database"]
usermdb = os.environ["user"]
pwdb = os.environ["password"]
sk = os.environ["sk"]
FLASK_RUN_HOST = os.environ["FLASK_RUN_HOST"]
FLASK_RUN_PORT = os.environ["FLASK_RUN_PORT"]
appinfo = os.environ["appinfo"]
creator = os.environ["creator"]
