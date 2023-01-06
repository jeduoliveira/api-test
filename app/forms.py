from flask_wtf import FlaskForm
from wtforms import StringField
from wtforms.validators import InputRequired

class ClienteForm(FlaskForm):
    nome = StringField('nome', validators=[InputRequired()])
    email = StringField('Email', validators=[InputRequired()])
    cpf = StringField('CPF', validators=[InputRequired()])
    tipo = StringField('Tipo')
    time_coracao = StringField('Time do Coração')
