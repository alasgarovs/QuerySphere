from app.main import app
from app.utils.create_super_user import createsuperuser
import argparse


def start_server():
    app.run(host='0.0.0.0', port=5000, debug=True)


def create_super_user(username, password):
    createsuperuser(username, password)


def main():
    parser = argparse.ArgumentParser(description='Run various scripts')
    subparsers = parser.add_subparsers(dest='command', help='Available commands')

    parser_startserver = subparsers.add_parser('startserver', help='Start the Flask server',
                                             description='Starts the Flask server')
    parser_createsuperuser = subparsers.add_parser('createsuperuser', help='Create a superuser',
                                                   description='Creates a superuser in the database')
    parser_createsuperuser.add_argument('--username', type=str, help='Superuser Username', required=True)
    parser_createsuperuser.add_argument('--password', type=str, help='Superuser Password', required=True)

    args = parser.parse_args()

    if args.command == 'startserver':
        start_server()
    elif args.command == 'createsuperuser':
        if not args.username or not args.password:
            parser.error("Username and password are required for 'createsuperuser' command")
        create_super_user(args.username, args.password)


if __name__ == '__main__':
    main()
