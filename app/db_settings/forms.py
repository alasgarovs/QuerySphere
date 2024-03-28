from flask_wtf import FlaskForm
from wtforms import StringField, SelectField
from wtforms.validators import DataRequired, Length


class CreateDBForm(FlaskForm):
    sql_type = SelectField('Select SQL Type', choices=[('mssql', 'Microsoft SQL Server'), ('psql', 'PostgreSQL')])
    server = StringField('Server', validators=[DataRequired(), Length(min=5, max=50)])
    database = StringField('Database', validators=[DataRequired(), Length(min=3, max=50)])
    username = StringField('Username', validators=[DataRequired(), Length(min=3, max=50)])
    password = StringField('Password', validators=[DataRequired(), Length(min=3, max=50)])
    driver = StringField('Driver (Microsoft SQL Server)', validators=[Length(min=0, max=50)])
    port = StringField('Port (PostgreSQL)', validators=[Length(min=0, max=50)])
