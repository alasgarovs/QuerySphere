from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, RadioField, BooleanField
from wtforms.validators import DataRequired, Length


class LoginForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired(), Length(min=3, max=12)],
                           render_kw={"placeholder": "Enter username"})
    password = PasswordField('Password', validators=[DataRequired(), Length(min=6, max=15)],
                             render_kw={"placeholder": "Enter password"})


class CreateUserForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired(), Length(min=3, max=12)])
    firstname = StringField('First Name', validators=[DataRequired(), Length(min=3, max=12)])
    lastname = StringField('Last Name', validators=[DataRequired(), Length(min=3, max=12)])
    usermode = RadioField('User Mode', choices=[('admin', 'admin'), ('user', 'user')], default='user')
    password = PasswordField('Password', validators=[DataRequired(), Length(min=6, max=15)])


class EditUserForm(CreateUserForm):
    password = PasswordField('Password', validators=[Length(min=0, max=15)])
    check_password = BooleanField("don't change password")
