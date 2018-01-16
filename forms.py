from flask_wtf import FlaskForm
from wtforms import TextField, TextAreaField, SubmitField, PasswordField, validators


"""
   Using FlaskForm to create Username, password, email 
   and submit for login/logout pages.  All fiels must be validated for length, 
   space and invalid characters,etc...
"""

class Forms(FlaskForm):
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


class Posts(FlaskForm):
    subject = TextField('Subject', validators=[
        validators.Length(min=1, max=50, message="Subject must be between 1 and 50 characters long"),
        validators.Required("Subject is required")
    ])

    message = TextAreaField('Message', validators=[
        validators.Length(min=1, message="Message must be at least one character long"),
        validators.Required('Message is required')
    ])
    
    post = SubmitField('Post')

