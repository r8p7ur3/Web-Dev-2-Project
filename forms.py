from flask import Flask
from flask_wtf import FlaskForm
from wtforms.validators import InputRequired, EqualTo
from wtforms import StringField, SubmitField, PasswordField, DateField, RadioField


 
class LoginForm(FlaskForm):
    userid = StringField("User ID:", validators = [InputRequired()])
    password = PasswordField("Password:", validators = [InputRequired()])
    submit = SubmitField("Submit")

class ProfileForm(FlaskForm):
    bio = StringField("Fill in your bio and let others know more about you:", validators = [InputRequired()])
    submit = SubmitField("Submit")

class MessageForm(FlaskForm):
    message = StringField("Type message here:", validators = [InputRequired()])
    submit = SubmitField("Submit")

class RegistrationForm(FlaskForm):
    userid = StringField("User ID:", validators = [InputRequired()])
    last_name = StringField("Surname:", validators = [InputRequired()])
    first_name = StringField("First name:", validators = [InputRequired()])
    age = DateField ("DOB:", format='%Y-%m-%d',validators=[InputRequired()])
    gender = RadioField("What do you identify as?",
        choices= ["Male", "Female", "Trans Male", "Trans Female", "Non-Binary", "Wombat", "Derek's Brother(Derek)", "Other"])
    password = PasswordField("Password:", validators = [InputRequired()])
    password2 = PasswordField("Confirm Password:", validators = [InputRequired(),EqualTo("password")])
   
    submit = SubmitField("Submit")