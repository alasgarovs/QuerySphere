from flask import Blueprint, render_template, redirect, url_for, flash, session, request, jsonify
from app.users.forms import CreateUserForm, EditUserForm
from app.users.models import db, Users
from functools import wraps

users_bp = Blueprint('users', __name__)



# CHECK LOGIN
####################################################
def login_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if session.get('username') is None:
            return redirect(url_for('login'))
        return f(*args, **kwargs)

    return decorated_function


# CHECK ADMIN STATUS
####################################################
def admin_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if session.get('username'):
            user = Users.query.filter_by(username=session.get('username')).first()
            if user and user.usermode == 'admin':
                return f(*args, **kwargs)
        flash("You don't have permission to access this section!", 'warning')
        return redirect(url_for('queries.queries'))

    return decorated_function


# USERS
####################################################
@users_bp.route('/', methods=['GET'])
@login_required
@admin_required
def users():
    username = session.get('username')
    all_users = Users.query.all()
    return render_template('users/users.html', username=username, users=all_users)


# GET USER
####################################################
@users_bp.route('/user/<user_id>', methods=['GET'])
@login_required
@admin_required
def get_user(user_id):
    username = session.get('username')
    form = EditUserForm()
    if user_id != 'add_user':
        user = Users.query.get_or_404(user_id)
        form.username.data = user.username
        form.firstname.data = user.firstname
        form.lastname.data = user.lastname
        form.usermode.data = user.usermode
    else:
        user=None
    return render_template('users/create-edit-user.html', username=username, form=form, user=user)


# ADD USER
####################################################
@users_bp.route('/user/add_user', methods=['POST'])
@login_required
@admin_required
def add_user():
    username = session.get('username')
    form = CreateUserForm()

    if form.validate_on_submit():
        user = Users.query.filter_by(username=form.username.data).first()
        if user:
            flash("Username already exists", 'danger')
        else:
            new_user = Users()
            new_user.username = form.username.data
            new_user.firstname = form.firstname.data
            new_user.lastname = form.lastname.data
            new_user.usermode = form.usermode.data
            new_user.set_password(form.password.data)
            
            db.session.add(new_user)
            db.session.commit()

            flash(f"'{form.username.data}' user added successfully", 'success')
            return redirect(url_for('users.users'))
    
    return render_template('users/create-edit-user.html', username=username, form=form)


# UPDATE USER
####################################################
@users_bp.route('/user/<int:user_id>', methods=['POST'])
@login_required
@admin_required
def update_user(user_id):
    username = session.get('username')
    form = EditUserForm()
    user = Users.query.get_or_404(user_id)
    if form.validate_on_submit():
        user.username = form.username.data
        user.firstname = form.firstname.data
        user.lastname = form.lastname.data
        user.usermode = form.usermode.data
        if form.check_password.data is True:
            pass
        else:
            if len(form.password.data) < 6:
                flash(f"Please check box or add new password!", 'danger')
                return render_template('users/create-edit-user.html', username=username, form=form, user=user)
            else:
                user.set_password(form.password.data)

        db.session.commit()

        flash(f"'{form.username.data}' user updated successfully", 'success')
        return redirect(url_for('users.users'))
    
    return render_template('users/create-edit-user.html', username=username, form=form, user=user)


# DELETE USER
####################################################
@users_bp.route('/user/<user_id>', methods=['DELETE'])
@login_required
@admin_required
def delete_user(user_id):
    user = Users.query.get_or_404(user_id)
    db.session.delete(user)
    db.session.commit()
    flash(f"'{user.username}' user deleted successfully", 'success')
    return '/users'
