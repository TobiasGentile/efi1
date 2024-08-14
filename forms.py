from flask_wtf import FlaskForm
from wtforms import StringField, FloatField, SelectField, SubmitField
from wtforms.validators import DataRequired
from models import Modelo, Categoria, Marca

class EquipoForm(FlaskForm):
    nombre = StringField('Nombre del Equipo', validators=[DataRequired()])
    modelo_id = SelectField('Modelo', coerce=int, validators=[DataRequired()])
    categoria_id = SelectField('Categoría', coerce=int, validators=[DataRequired()])
    marca_id = SelectField('Marca', coerce=int, validators=[DataRequired()])
    costo = FloatField('Costo', validators=[DataRequired()])
    submit = SubmitField('Guardar')

    def populate_choices(self):
        self.modelo_id.choices = [(m.id, m.nombre) for m in Modelo.query.all()]
        self.categoria_id.choices = [(c.id, c.nombre) for c in Categoria.query.all()]
        self.marca_id.choices = [(m.id, m.nombre) for m in Marca.query.all()]
