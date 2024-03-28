# Query Sphere

Welcome to Query Sphere! A small [Flask](https://flask.palletsprojects.com/en/2.2.x/tutorial/) application. Run SQL queries with a click.

### About the application

Query Sphere application was created to analyze data without requiring knowledge of SQL code. Normally, companies need to write SQL queries to analyze data stored in databases. With this app you don't need to run SQL code over and over again when analyzing data. Users can easily run the queries they want in a graphical interface to analyze the data. This provides convenience to users and allows them to run queries dynamically in the graphical interface. The application being locally web-based means it can be accessed from various devices.

### Features

List of key features of Query Sphere

- User management and permissions
- Query management
- Configuring multiple database connections: PostgreSQL, MSSQL, etc.
- Graphical interface for query execution
- Downloading the executed query in excel format
- Natively web-based for cross-device accessibility 

### How to Install?
Clone the repository and Use virtualenv as:
```console
python3 -m venv .venv
source .venv/bin/activate
```

Install requirements:
```console
pip install -r requirements.txt
```

#### Database Initialization
Before running the application, initialize the database:
```console
flask db init
flask db migrate -m 'add commit'
flask db upgrade
```

#### Create admin user for login
Create admin user by running this command and the user will be created:
- user: ```admin``` ; passwd: ```admin.0101```
```console
python app/utils/create_admin.py
```

#### Running the Application
To run the application, execute the following command:
```console
python run.py
```
After running the application, you can log in with default credentials and manage users, create or run queries and etc.

### Contribution

Contributions welcome! Feel free to contribute, report issues, make your changes. I appreciate your help in improving Query Sphere. Let's make this project even better together!

### License

This project is licensed under the [MIT License](LICENSE).
