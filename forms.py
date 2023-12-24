from flask_wtf import FlaskForm
from flask_wtf.file import FileField, FileRequired, FileAllowed, FileSize
from wtforms.fields import StringField, IntegerField, SubmitField, TextAreaField, PasswordField, RadioField, DateField, BooleanField
from wtforms.validators import DataRequired, length, equal_to
class AddProductForm(FlaskForm):
    name = StringField("Product Name", validators=[DataRequired()])
    price = IntegerField("Price", validators=[DataRequired()])
    img = FileField("Image Name", validators=[
        FileRequired(),
        FileAllowed(["jpeg", "jpg", "png"]),
        FileSize(1024 * 1014 * 20)
    ])
    game = FileField("Your Game", validators=[
        FileRequired(),
        FileAllowed(["zip", "zpaq", "rar"])
    ])
    about_game = TextAreaField("Tell us something about game")

    submit = SubmitField("Submit")

class EditProductForm(FlaskForm):
    name = StringField("Product Name", validators=[])
    price = IntegerField("Price", validators=[])
    img = FileField("Image Name", validators=[
        FileAllowed(["jpeg", "jpg", "png"]),
        FileSize(1024 * 1014 * 50)
    ])
    game = FileField("Your Game", validators=[
        FileAllowed(["zip", "zpaq", "rar"])
    ])
    about_game = TextAreaField("Tell us something about the game")
    submit = SubmitField("Submit")

class RegistrForm(FlaskForm):
    username = StringField("Enter a username")
    password = PasswordField("Enter the password",validators=[length(min=8, max=12)])
    repeate_password = PasswordField("Repeat the password", validators=[equal_to("password")])
    gender = RadioField("Please indicate your gender", choices=["Female", "Male"])
    birthday = DateField("Date of birth")
    submit = SubmitField("Registre")
class LoginForm(FlaskForm):
    username = StringField("Enter a username", validators=[DataRequired()])
    password = PasswordField("Enter the password", validators=[DataRequired()])

    submit = SubmitField("Log In")

class IsDisplayedForm(FlaskForm):
    checkbox = BooleanField('Will this product be on the market?', validators=[DataRequired()])
    submit = SubmitField("Appear")