from flask import Blueprint, render_template, redirect, url_for, flash, session, request, json
from app.queries.forms import CreateQueryForm
from app.queries.models import db, Reports
from app.users.models import Users
from app.users.views import login_required, admin_required

queries_bp = Blueprint('queries', __name__)


# QUERIES
###################################################
@queries_bp.route('/queries')
@login_required
def queries():
    username = session.get('username')
    user = Users.query.filter_by(username=username).first()
    all_queries = Reports.query.all()
    return render_template('queries/queries.html', username=username, queries=all_queries, user=user)


# CREATE QUERY
####################################################
@queries_bp.route('/queries/create-query', methods=['GET', 'POST'])
@login_required
@admin_required
def create_query():
    username = session.get('username')
    form = CreateQueryForm()

    if request.method == 'POST' and form.validate_on_submit():
        table_data = request.form.get('tableData')
        table_data = json.loads(table_data)

        new_query = Reports()
        new_query.query_name = form.query_name.data
        new_query.query_description = form.query_description.data
        new_query.query_text = form.query_text.data
        new_query.variable_list = json.dumps(table_data)

        db.session.add(new_query)
        db.session.commit()

        flash('Query created successfully', 'success')
        return redirect(url_for('queries.queries'))

    return render_template('queries/create-edit-query.html', username=username, form=form)


# EDIT QUERY
####################################################
@queries_bp.route('/queries/query/<int:query_id>', methods=['GET', 'POST'])
@login_required
@admin_required
def edit_query(query_id):
    username = session.get('username')
    form = CreateQueryForm()
    query = Reports.query.get_or_404(query_id)
    if request.method == 'POST' and form.validate_on_submit():
        table_data = request.form.get('tableData')
        table_data = json.loads(table_data)

        query.query_name = form.query_name.data
        query.query_description = form.query_description.data
        query.query_text = form.query_text.data
        query.variable_list = json.dumps(table_data)

        db.session.commit()

        flash('Query updated successfully', 'success')
        return redirect(url_for('queries.queries'))
    else:
        form.query_name.data = query.query_name
        form.query_description.data = query.query_description
        form.query_text.data = query.query_text

        variable_list = json.loads(query.variable_list) if query.variable_list else []
        n = 1
        data = []
        for variable in variable_list:
            data.append([n, variable['Name'], variable['Type']])
            n += 1
        return render_template('queries/create-edit-query.html', username=username, form=form, query=query,
                               variable_list=data)


# DELETE QUERY
####################################################
@queries_bp.route('/queries/query/<int:query_id>/delete')
@login_required
@admin_required
def delete_query(query_id):
    query = Reports.query.get_or_404(query_id)
    db.session.delete(query)
    db.session.commit()
    flash(f"'{query.query_name}' query deleted successfully", 'success')
    return redirect(url_for('queries.queries'))
