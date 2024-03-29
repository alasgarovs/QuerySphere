import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..')))
from app.main import app, db, Users
from colorama import Fore


def username_exists(username):
    return db.session.query(db.exists().where(Users.username == username)).scalar()


def control_credentials(username, password):
    if not (2 < len(username) < 13):
        return False, "Username must be between 3 and 12 characters long"

    if not (5 < len(password) < 16):
        return False, "Password must be between 6 and 15 characters long"

    return True, "Credentials are valid."


def createsuperuser(username, password):
    valid, message = control_credentials(username, password)
    if valid:
        with app.app_context():
            if username_exists(username):
                print(Fore.LIGHTRED_EX, "Username already exists, try different username", Fore.RESET)
            else:
                admin = Users(username=username,
                              firstname=username,
                              lastname=username,
                              usermode='admin')
                admin.set_password(password)
                db.session.add(admin)
                db.session.commit()
                print(Fore.LIGHTGREEN_EX, f"{username} user created successfully.", Fore.RESET)
    else:
        print(Fore.RED, message, Fore.RESET, sep='')
