from app.main import app
from app.utils.createadmin import createadmin
import argparse


def run_server():
    app.run(host='0.0.0.0', port=5000, debug=True)


def create_admin(username, password):
    createadmin(username, password)


def main():
    parser = argparse.ArgumentParser(description='Run various scripts')
    parser.add_argument('command', choices=['runserver', 'createadmin'], help='Command to execute')
    parser.add_argument('--username', type=str, help='Admin username')
    parser.add_argument('--password', type=str, help='Admin password')

    args = parser.parse_args()

    if args.command == 'runserver':
        run_server()
    elif args.command == 'createadmin':
        if not args.username or not args.password:
            parser.error("Username and password are required for 'createadmin' command.")
        create_admin(args.username, args.password)


if __name__ == '__main__':
    main()
