from app.extensions import db
from datetime import datetime


class Reports(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    query_name = db.Column(db.String(20), unique=True, nullable=False)
    query_description = db.Column(db.String(50), nullable=False)
    variable_list = db.Column(db.String(1000), nullable=False)
    query_text = db.Column(db.String(1000), nullable=False)
    date = db.Column(db.DateTime, default=datetime.utcnow)

    def __repr__(self):
        return f"<Report {self.query_name}>"

