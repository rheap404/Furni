from flask_wtf import FlaskForm
from wtforms import IntegerField, StringField, PasswordField, SubmitField
from wtforms.validators import InputRequired, Length, ValidationError


class LoginForm(FlaskForm):
    email=StringField('email', validators=[
        InputRequired(), Length(min=10, max=40)], render_kw={"placeholder":"Email"})
    
    password=PasswordField('password', validators=[
        InputRequired(), Length(min=4, max=25)], render_kw={"placeholder":"Password"})
    
    submit=SubmitField("Login")
    
    
class RegisterForm(FlaskForm):
    name=StringField('name', validators=[
        InputRequired(), Length(min=0, max=25)], render_kw={"placeholder":"Name"})
    
    email=StringField('email', validators=[
        InputRequired(), Length(min=10, max=40)], render_kw={"placeholder":"Email"})
    
    password=PasswordField('password', validators=[
        InputRequired(), Length(min=4, max=20)], render_kw={"placeholder":"Password"})
    
    submit=SubmitField("Register")
    
 
        

