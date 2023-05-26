import os

from dotenv import load_dotenv, find_dotenv

load_dotenv(find_dotenv())


basedir = os.path.abspath(os.path.dirname(__file__))

DB_USER = os.getenv('DB_USER')
DB_PASSWORD = os.getenv('DB_PASSWORD')
DB_NAME = os.getenv('DB_NAME')

os.environ['DATABASE_URL'] = os.getenv('DATABASE_URL').format(DB_USER, DB_PASSWORD, DB_NAME)
os.environ['FLASK_APP'] = os.getenv('FLASK_APP')


class Config(object):
    DEBUG = False
    TESTING = False
    CSRF_ENABLED = True
    SQLALCHEMY_DATABASE_URI = os.environ['DATABASE_URL']


class ProductionConfig(Config):
    DEBUG = False


class StagingConfig(Config):
    DEVELOPMENT = True
    DEBUG = True


class DevelopmentConfig(Config):
    DEVELOPMENT = True
    DEBUG = True


class TestingConfig(Config):
    TESTING = True


config = ProductionConfig()
config_str = os.getenv('SRC_ENV', 'prod')
if config_str == 'dev':
    config = DevelopmentConfig()
elif config_str == 'test':
    config = TestingConfig()
else:
    config = ProductionConfig()