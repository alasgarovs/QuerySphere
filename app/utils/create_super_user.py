import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..')))
from app.main import app, db, Users


def username_exists(username):
    return db.session.query(db.exists().where(Users.username == username)).scalar()


def createadmin(username, password):
    with app.app_context():
        if username_exists(username):
            print("Username already exists")
        else:
            admin = Users(username=username, firstname='admin', lastname='admin', usermode='admin')
            admin.set_password(password)
            db.session.add(admin)
            db.session.commit()
            print(f"{username} user created successfully.")
