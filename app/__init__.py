from flask import Flask
from config import app_config
from flask_migrate import Migrate
from .models import *

from .routes import user as user_blueprint
from .routes import tweet as tweet_blueprint
from .routes import profile as profile_blueprint

def create_app(config_name):
    app = Flask(__name__, instance_relative_config=True)
    app.config.from_object(app_config[config_name])
    app.config.from_pyfile('config.py')

    db.init_app(app)
    migrate = Migrate(app, db)

    app.register_blueprint(user_blueprint, url_prefix='/user')
    app.register_blueprint(tweet_blueprint, url_prefix='/tweet')
    app.register_blueprint(profile_blueprint, url_prefix='/profile')

    return app
