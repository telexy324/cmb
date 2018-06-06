import os
basedir = os.path.abspath(os.path.dirname(__file__))


class Config:
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'hard to guess string'
    SQLALCHEMY_COMMIT_ON_TEARDOWN = True
    FLASKY_ADMIN = os.environ.get('FLASKY_ADMIN')
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SQLALCHEMY_RECORD_QUERIES = True
    SQLALCHEMY_DATABASE_URI = os.environ.get('DEV_DATABASE_URL') or \
        'mysql://root:#EDCFT^7ujmnbv@192.168.30.42/cmb'
    SQLALCHEMY_BINDS = {
        'users': 'oracle://bill:bill@192.168.30.15:1521/orcl_dg1'
    }
    #WTF_CSRF_CHECK_DEFAULT = False

    @staticmethod
    def init_app(app):
        pass


class DevelopmentConfig(Config):
    DEBUG = True


class TestingConfig(Config):
    TESTING = True


class ProductionConfig(Config):
    SQLALCHEMY_DATABASE_URI = os.environ.get('DEV_DATABASE_URL') or \
        'mysql://root:#EDCFT^7ujmnbv@192.168.30.42/cmb'
    SQLALCHEMY_BINDS = {
        'users': 'oracle://bill:bill@192.168.30.15:1521/orcl_dg1'
    }
config = {
    'development': DevelopmentConfig,
    'testing': TestingConfig,
    'production': ProductionConfig,

    'default': DevelopmentConfig
}