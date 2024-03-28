import sys
import os

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..')))
from app.main import app, db, Users


def username_exists(username):
    return db.session.query(db.exists().where(Users.username == username)).scalar()


with app.app_context():
    if username_exists('admin'):
        print("Username 'admin' already exists. Cannot create user.")
    else:
        admin = Users(username='admin', firstname='admin', lastname='admin', usermode='admin')
        admin.set_password('admin.0101')
        db.session.add(admin)
        db.session.commit()
        print("User 'admin' created successfully.")
