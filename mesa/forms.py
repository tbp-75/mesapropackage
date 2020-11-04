from flask_wtf import FlaskForm
# from flask_table import Table, Col
from wtforms import IntegerField, FloatField, SubmitField, StringField, SelectField
from wtforms.validators import DataRequired, ValidationError, NumberRange, InputRequired, length


class PredictionForm(FlaskForm):
    pregnancies = IntegerField("Number of Pregnancies", 
                                validators=[DataRequired()], description = 'from 0 to 20')

    glucose = FloatField("Glucose", 
                                validators=[DataRequired()], description= 'from 30 to 300')

    bloodpressure = IntegerField("Blood Pressure", 
                                validators=[DataRequired()], description= 'from 20 to 200')

    skinthickness = IntegerField("Skin Thickness", 
                                validators=[DataRequired()], description= 'from 5 to 100')

    insulin = IntegerField("Insulin Level", 
                                validators=[DataRequired()], description= 'from 10 to 1000')

    bmi = FloatField("Body Mass Index", 
                                validators=[DataRequired()], description= 'from 10 to 100')

    diabetespedigree = FloatField("Diabetes Pedigree Function", 
                                validators=[DataRequired()], description= 'from 0.03 to 3')

    age = IntegerField("Age", 
                                validators=[DataRequired()], description= 'from 10 to 100')

    
    submit = SubmitField('Predict')

class ProductsForm(FlaskForm):
    name = StringField("Product", validators=[InputRequired(), length(min=3, max=20)])
    price_per_gm = FloatField("Price per gm", validators=[NumberRange(min=0, max=1000000)])
    quantity = IntegerField("Quantity", validators=[NumberRange(min=0, max=1000000)])

    edit = SubmitField('Edit')
    search = SubmitField('Search')
    add = SubmitField('Add')
    delete = SubmitField('Delete')

