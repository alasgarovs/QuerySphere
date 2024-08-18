from flask import Flask, render_template, request, flash, redirect, url_for, session, json
from flask_migrate import Migrate
from flask import send_file
from .extensions import db
from app.users.forms import LoginForm
from app.users.models import Users
from app.queries.models import Reports
from app.db_settings.models import DataBase
from app.utils.server_connections import connect_postgresql
from app.users.views import users_bp, login_required
from app.queries.views import queries_bp
from app.db_settings.views import db_settings_bp
import pandas as pd
import secrets
import string
import os

app = Flask(__name__)
app.secret_key = 'b00a77b0ec653f776b80d0ff78ead01a75ce1d32fbd09541d892cdb1b1d86474'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///default.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False


db.init_app(app)
migrate = Migrate(app, db)


# RANDOM TOKEN
####################################################
def generate_random_token(length):
    alphabet = string.ascii_letters + string.digits
    return ''.join(secrets.choice(alphabet) for _ in range(length))


# CONVERT TIMEZONE
####################################################
def convert_timezone_unaware(df):
    for column in df.columns:
        if pd.api.types.is_datetime64_any_dtype(df[column]):
            df[column] = df[column].dt.tz_localize(None)
    return df


# EXPORT QUERY TO EXCEL
####################################################
@app.route('/queries/export-query/<file_name>', methods=['GET'])
@login_required
def export_query(file_name):
    excel_file_path = os.path.join("exported_queries", f"{file_name}.xlsx")
    absolute_path = os.path.abspath(excel_file_path)

    return send_file(absolute_path, as_attachment=True)


# RUN QUERY
####################################################
@queries_bp.route('/queries/run-query/<int:query_id>', methods=['GET', 'POST'])
@login_required
def run_query(query_id):
    query = Reports.query.get_or_404(query_id)
    username = session.get('username')
    variable_list = json.loads(query.variable_list)
    server = DataBase.query.filter_by(id=1).first()
    if server:
        pass
    else:
        flash('First configure connection settings and after run query!', 'danger')
        return redirect(url_for('db_settings.db_settings'))
    query_result = None
    columns = None
    if request.method == 'POST':
        # This section will be update
        ######################################
        parameter_declarations = ""
        for variable in variable_list:
            parameter_declarations += f"DECLARE @{variable['Name']} {variable['Type']}\n"
        parameter_declarations += "\n"
        for variable in request.form:
            parameter_declarations += f"SET @{variable} = '{request.form[variable]}'\n"
        parameter_declarations += "\n" + query.query_text

        if server.sql_type == 'psql':
            query_result, columns = connect_postgresql(server.database,
                                                       server.username,
                                                       server.password,
                                                       server.server,
                                                       server.port,
                                                       parameter_declarations)
        else:
            flash(f'Server connection error: {str(server.sql_type).upper()}', 'danger')
        ########################################

        if query_result and columns:
            token = generate_random_token(10)
            query_name = query.query_name + '_' + token

            df = pd.DataFrame(query_result, columns=columns)
            df = convert_timezone_unaware(df)

            excel_file_path = f"exported_queries/{query_name}.xlsx"
            df.to_excel(excel_file_path, index=False)

            flash('Query executed successfully', 'success')
            return render_template('queries/run-query.html',
                                   username=username,
                                   query=query,
                                   variable_list=variable_list,
                                   token=token,
                                   columns=columns,
                                   query_result=query_result)
        else:
            pass

    return render_template('queries/run-query.html', username=username, query=query, variable_list=variable_list)


# LOGIN
####################################################
@app.route('/', methods=['GET', 'POST'])
def login():
    username = session.get('username')
    form = LoginForm()
    if request.method == 'POST' and form.validate_on_submit():
        username = form.username.data
        password = form.password.data
        user = Users.query.filter_by(username=username).first()
        if user and user.check_password(password):
            session['username'] = username
            flash(f'Welcome {username}', 'success')
            return redirect(url_for('queries.queries'))
        else:
            flash('Invalid username or password. Please try again!', 'danger')
            username = None

    return render_template('main.html', username=username, form=form)


# LOGOUT
####################################################
@app.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('queries.queries'))


app.register_blueprint(users_bp, url_prefix='/users')
app.register_blueprint(queries_bp)
app.register_blueprint(db_settings_bp)

