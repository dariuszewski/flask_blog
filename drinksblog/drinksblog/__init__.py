from flask import Flask, Blueprint
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from flask_login import LoginManager
from drinksblog.config import Config


db = SQLAlchemy()
bcrypt = Bcrypt()
login_manager = LoginManager()
login_manager.login_view = 'users.login'
login_manager.login_message = 'Zaloguj się aby odwiedzić tą stronę.'
login_manager.login_message_category = 'info'





def create_app(config_class=Config):
    app = Flask(__name__, instance_relative_config=True)
    app.config.from_object(Config)


    db.init_app(app)
    bcrypt.init_app(app)
    login_manager.init_app(app)


    from drinksblog.users.routes import users
    app.register_blueprint(users)

    from drinksblog.posts.routes import posts
    app.register_blueprint(posts)

    from drinksblog.conversations.routes import conversations
    app.register_blueprint(conversations)

    from drinksblog.main.routes import main
    app.register_blueprint(main)

    return app
