
import os

class Config:
    SECRET_KEY = "super-secret"
    SQLALCHEMY_DATABASE_URI = "sqlite:///data.db"
    SQLALCHEMY_TRACK_MODIFICATIONS = False






# import os

# class Config:
#     SECRET_KEY = os.environ.get('SECRET_KEY', 'fdgrd234@rr#3jfd')
#     SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL', 'sqlite:///site.db')
#     SQLALCHEMY_TRACK_MODIFICATIONS = False
#     DEBUG = False
#     TESTING = False

# class DevelopmentConfig(Config):
#     DEBUG = True
#     SQLALCHEMY_DATABASE_URI = os.environ.get('DEV_DATABASE_URL', 'sqlite:///dev_site.db')

# class TestingConfig(Config):
#     TESTING = True
#     SQLALCHEMY_DATABASE_URI = os.environ.get('TEST_DATABASE_URL', 'sqlite:///test_site.db')

# class ProductionConfig(Config):
#     SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL', 'sqlite:///prod_site.db')
