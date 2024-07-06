from flask import Flask, jsonify
from flask_sqlalchemy import SQLAlchemy
from config import Config
from flask_bcrypt import Bcrypt
from flask_jwt_extended import JWTManager

app = Flask(__name__)
app.config.from_object(Config)
db = SQLAlchemy(app)
bcrypt = Bcrypt(app)
jwt = JWTManager(app)


@app.route('/', methods=['GET'])
def home():
    return jsonify({"message": "Welcome to backend stage two task for the HNG Internship"})

from app.routes import *
app.register_blueprint(auth_bp)
app.register_blueprint(user_bp)
app.register_blueprint(org_bp)