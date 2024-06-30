from flask_wtf import FlaskForm
from wtforms.fields import StringField, PasswordField, SubmitField, TextAreaField, SelectField, HiddenField
from wtforms.validators import DataRequired, Length, EqualTo
from flask_wtf.file import FileField, FileRequired, FileSize, FileAllowed


class RegisterForm(FlaskForm):
    username = StringField("Username", validators=[DataRequired()])
    password = PasswordField("Password", validators=[DataRequired(), Length(min=8, max=15, message="Password must be at least 8 characters long")])
    repeat_password = PasswordField("Repeat password", validators=[DataRequired(), EqualTo("password", message="Passwords must match")])
    image = FileField(validators=[FileAllowed(['jpg','jpeg','png','webp','heif'], message="Only Images Allowed")])
    submit = SubmitField()

class LoginForm(FlaskForm):
    username = StringField("Username", validators=[DataRequired()])
    password = PasswordField("Password", validators=[DataRequired()])
    login = SubmitField()

class PostForm(FlaskForm):
    title = StringField("Post Title", validators=[DataRequired()])
    post = TextAreaField("Post Content", validators=[DataRequired()])
    image = FileField(validators=[FileAllowed(['jpg','jpeg','png','webp','heif'], message="Only Images Allowed")]) 
    post_type = SelectField('Choose A Post Type', choices=[
        ('general', 'General Forum'),
        ('theory', 'Music Theory'),
        ('production', 'Music Production'),
        ('mixing', 'Music Mixing'),
        ('mastering', 'Music Mastering')],
         validators=[DataRequired()])
    referrer = HiddenField()
    submit = SubmitField()

class CommentForm(FlaskForm):
    comment = StringField("Comment", validators=[Length(min=1, message="Minimum 1 characters")])
    submit = SubmitField("Comment")
