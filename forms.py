from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, PasswordField, BooleanField
from wtforms.validators import DataRequired, URL
from flask_ckeditor import CKEditorField

class AddNewItemForm(FlaskForm):
    name = StringField("New Item Name", validators=[DataRequired()])
    add_item = SubmitField("Add New Item")
class LoginForm(FlaskForm):
    name = StringField("Name", validators=[DataRequired()])
    password = PasswordField("Password", validators=[DataRequired()])
    login_in = SubmitField("Log me in!")

class TakeItem(FlaskForm):
    take_item = BooleanField()

class ConfirmForm(FlaskForm):
    confirm = SubmitField("Take Items")