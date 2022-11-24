from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, PasswordField, BooleanField
from wtforms.validators import DataRequired, URL, Length, Email, EqualTo
from flask_ckeditor import CKEditorField

class AddNewItemForm(FlaskForm):
    name = StringField("New Item Name", validators=[DataRequired()])
    add_item = SubmitField("Add New Item")
class LoginForm(FlaskForm):
    name = StringField("Name", validators=[DataRequired()])
    password = PasswordField("Password", validators=[DataRequired()])
    remember = BooleanField("Remember Me")
    login_in = SubmitField("Log me in")

class RegisterForm(FlaskForm):
    name = StringField("Name", validators=[DataRequired(), Length(min=2, max=20)])
    email = StringField("Email", validators=[DataRequired(), Email()])
    password = PasswordField("Password", validators=[DataRequired()])
    confirm_password = PasswordField("Confirm password", validators=[DataRequired(), EqualTo("password")])
    register = SubmitField("Register")


