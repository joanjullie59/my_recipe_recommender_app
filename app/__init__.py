import os
from flask import Flask, render_template
from flask_login import LoginManager
from dotenv import load_dotenv
from .models import db, User
from .extensions import cache, limiter

load_dotenv()  # Load .env variables

login_manager = LoginManager()

def create_app():
    app = Flask(__name__)
    app.config.from_object('config.Config')

    db.init_app(app)
    cache.init_app(app)
    limiter.init_app(app)
    login_manager.init_app(app)
    login_manager.login_view = 'auth.login'

    @login_manager.user_loader
    def load_user(user_id):
        return User.query.get(int(user_id))

    from .auth import auth_bp
    app.register_blueprint(auth_bp)

    with app.app_context():
        db.create_all()

    @app.route('/')
    def home():
        if not User.query.first():
            return render_template('index.html')
        return render_template('index.html')

    return app
