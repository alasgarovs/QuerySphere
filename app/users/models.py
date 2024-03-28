from app.extensions import db
from flask_bcrypt import Bcrypt
from datetime import datetime

bcrypt = Bcrypt()


class Users(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(12), unique=True, nullable=False)
    firstname = db.Column(db.String(12), nullable=False)
    lastname = db.Column(db.String(12), nullable=False)
    password_hash = db.Column(db.String(30), nullable=False)
    usermode = db.Column(db.String(5), nullable=False)
    date = db.Column(db.DateTime, default=datetime.utcnow)

    def __repr__(self):
        return f"<User {self.username}>"

    def set_password(self, password):
        self.password_hash = bcrypt.generate_password_hash(password).decode('utf-8')

    def check_password(self, password):
        return bcrypt.check_password_hash(self.password_hash, password)

