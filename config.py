from password import MYPASSWORD

class DevelopmentConfig:
    SQLALCHEMY_DATABASE_URI = f'mysql+mysqlconnector://root:{MYPASSWORD}@localhost/factory_db'
    CACHE_TYPE = 'SimpleCache'
    DEBUG = True