from dotenv import load_dotenv
import os

load_dotenv()

host = os.environ.get["host"]
database = os.environ.get["database"]
usermdb = os.environ.get["user"]
pwdb = os.environ.get["password"]
sk = os.environ.get["sk"]
FLASK_RUN_HOST = os.environ.get["FLASK_RUN_HOST"]
FLASK_RUN_PORT = os.environ.get["FLASK_RUN_PORT"]
creator = os.environ.get["creator"]
