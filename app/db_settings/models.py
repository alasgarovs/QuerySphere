from app.extensions import db
from datetime import datetime


class DataBase(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    sql_type = db.Column(db.String(20), unique=True, nullable=False)
    server = db.Column(db.String(50), nullable=False)
    database = db.Column(db.String(50), nullable=False)
    username = db.Column(db.String(50), nullable=False)
    password = db.Column(db.String(50), nullable=False)
    driver = db.Column(db.String(50), default=None, nullable=True)
    port = db.Column(db.String(10), default=None, nullable=True)
    date = db.Column(db.DateTime, default=datetime.utcnow)

    def __repr__(self):
        return f"<SQL {self.sql_type}>"
