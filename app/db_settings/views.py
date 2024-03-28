from flask import Blueprint, render_template, redirect, url_for, flash, session, request
from app.db_settings.forms import CreateDBForm
from app.db_settings.models import db, DataBase
from app.users.views import login_required, admin_required

db_settings_bp = Blueprint('db_settings', __name__)


# DB SETTINGS
####################################################
@db_settings_bp.route('/db_settings', methods=['GET', 'POST'])
@login_required
@admin_required
def db_settings():
    username = session.get('username')

    form = CreateDBForm()
    server = DataBase.query.filter_by(id=1).first()
    if server:
        pass
    else:
        server = DataBase()
    if request.method == 'POST' and form.validate_on_submit():
        server.sql_type = form.sql_type.data
        server.server = form.server.data
        server.database = form.database.data
        server.username = form.username.data
        server.password = form.password.data
        if server.sql_type == 'mssql':
            server.driver = 'mssqldriver'
            server.port = None
        else:
            server.driver = None
            server.port = '5432'

        db.session.add(server)
        db.session.commit()

        flash("Database connection settings updated successfully", 'success')
        return redirect(url_for('queries.queries'))
    else:
        form.sql_type.data = server.sql_type
        form.server.data = server.server
        form.database.data = server.database
        form.username.data = server.username
        form.password.data = server.password

        return render_template('db_settings/db_settings.html', username=username, form=form)
