from flask_wtf import FlaskForm
from wtforms import TextField, TextAreaField, SubmitField, PasswordField, validators


"""
   Using FlaskForm to create Username, password, email 
   and submit for login/logout pages.  All fiels must be validated for length, 
   space and invalid characters,etc...
"""

class CreateForm(FlaskForm):
    username = TextField('Username', validators=[
        validators.Length(min=3,max=20,message="Username must be between 3 and 30 characters long"), 
        validators.Required("User name is required"),
        validators.Regexp('\w+$', message="Username must contain only letters,numbers or underscore") 
    ])

    password1 = PasswordField('Password', validators=[ 
        validators.Length(min=3,max=20, message="Password must be between 3 and 20 characters long"), 
        validators.Required("Password is required"),
        validators.Regexp('[a-zA-Z0-9_+=\[{\]}@#$%&!-+(~)*]+$',message="Password contains invalid character!")
    ])

    password2 = PasswordField('Confirm Password', [ 
        validators.Required("Invalid password"),
        validators.EqualTo('password1', message="Password mismatched!!!")
    ]) 

    email = TextField('Email', validators=[ 
        validators.Optional(), 
        validators.Length(min=3,max=20, message="Email must be between 3 and 20 characters long"), 
        validators.Regexp('[a-zA-Z0-9_.@]+$',message="Email contains invalid character!"),
        validators.Email("Please enter valid email!!!")
    ]) 

    submit = SubmitField('Create an account')
    login = SubmitField('Login')

