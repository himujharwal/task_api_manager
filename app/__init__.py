from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from app.config import Config


db = SQLAlchemy()

def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)
    db.init_app(app)

    with app.app_context():
        from app import routes
        # db.drop_all()
        db.create_all()


    return app





# from .config import DevelopmentConfig
# from .models import db

# from .auth import auth_bp
# from .task import task_bp


# def create_app():
#     app = Flask(__name__)
#     app.config.from_object(DevelopmentConfig)  #It copies all the variables from DevelopmentConfig into app.config

#     db.init_app(app)

#     app.register_blueprint(task_bp)
#     app.register_blueprint(auth_bp)

#     with app.app_context():
#         db.create_all()

#     return app
