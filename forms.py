from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, PasswordField
from wtforms.validators import DataRequired, URL
from flask_ckeditor import CKEditorField

class AddNewItemForm(FlaskForm):
    name = StringField("New Item Name", validators=[DataRequired()])
    add_item = SubmitField("Add New Item")