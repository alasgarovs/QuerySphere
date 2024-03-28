from flask_wtf import FlaskForm
from wtforms import StringField, SelectField, TextAreaField
from wtforms.validators import DataRequired, Length

variable_type_choices = [('', 'Select Variable Type'),
                         ('INT', 'INT'),
                         ('VARCHAR', 'VARCHAR'),
                         ('DATE', 'DATE'),
                         ('DATETIME', 'DATETIME')]


class CreateQueryForm(FlaskForm):
    query_name = StringField('Query Name', validators=[DataRequired(), Length(min=5, max=50)])
    query_description = StringField('Description', validators=[DataRequired(), Length(min=5, max=50)])
    declare_name = StringField('Variable Name')
    variable_type = SelectField('Variable Type', choices=variable_type_choices)
    query_text = TextAreaField('Query', validators=[DataRequired()])
