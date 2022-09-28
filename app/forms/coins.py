from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, SelectField, DecimalField
from wtforms.validators import DataRequired,  NumberRange
from app.views_class.Read import Read

read = Read()
names = read.get_saved_coin_names()


class AddForm(FlaskForm):
    name = SelectField('name', choices=names)
    quantity = DecimalField('Value', validators=[DataRequired(), NumberRange(min=0, max=100000)])
    value = StringField('Value', validators=[DataRequired()])
    submit = SubmitField('Add')


class DeleteForm(FlaskForm):
    name = SelectField('name')
    quantity = DecimalField('Value', validators=[DataRequired(), NumberRange(min=0, max=100000)])
    delete = SubmitField('Delete')
