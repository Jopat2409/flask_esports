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

    APP_DEBUG = True
    APP_TESTING = False

def set_endpoint_directory(dir_: str) -> None:
    Config.API_ENDPOINT_DIR = dir_

def set_debug(debug: bool) -> None:
    Config.APP_DEBUG = debug

def set_testing(testing: bool) -> None:
    Config.APP_TESTING = testing
