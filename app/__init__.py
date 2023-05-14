from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager, UserMixin
from config import Config

app = Flask(__name__)
app.config.from_object(Config)
db = SQLAlchemy(app)

from app import routes, models, forms

login_manager = LoginManager(app)

@login_manager.user_loader
def load_user(user_id):
    # Load user from database or other data source
    return models.User.query.get(int(user_id))

with app.app_context():
    db.create_all()