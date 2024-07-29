import os

from dotenv import load_dotenv

load_dotenv()

basedir = os.path.abspath(os.getcwd())
module_basedir = os.path.abspath(os.path.dirname(__file__))

class Config:

    SECRET_KEY = os.environ.get('SECRET_KEY')

    MODULE_BASE_DIR = module_basedir

    BASE_DIRECTORY = basedir
    API_ENDPOINT_DIR = os.path.join(BASE_DIRECTORY, "endpoints")
    SQL_DATABASE_URI = os.environ.get("SQL_DATABASE_URI") or os.path.join(BASE_DIRECTORY, "app.db")

    DEBUG = True
    TESTING = False
