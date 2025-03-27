from flask_sqlalchemy import SQLAlchemy
from werkzeug.security import generate_password_hash, check_password_hash

db = SQLAlchemy()

class Users(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    first_name = db.Column(db.String(50))
    last_name = db.Column(db.String(50))
    email = db.Column(db.String(100), unique=True, nullable=False)
    password = db.Column(db.String(255), nullable=False)
    decks = db.relationship('Decks', backref="owner", lazy=True)

    def set_password(self, password):
        self.password = generate_password_hash(password)

    def check_password(self, password):
         return check_password_hash(self.password, password)

class Decks(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    id_user = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)  
    name = db.Column(db.String(50))
    description = db.Column(db.String(100))
    cards = db.relationship('Cards', backref="deck", lazy=True)

class Cards(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    id_deck = db.Column(db.Integer, db.ForeignKey('decks.id'), nullable=False) 
    front = db.Column(db.String(50))
    back = db.Column(db.String(50))
    known = db.Column(db.Boolean, default=False)

def init_db(app):
    db.init_app(app)
    with app.app_context():
        db.create_all()
