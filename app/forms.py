from flask.ext.wtf import Form
from wtforms import TextField, StringField, BooleanField, SelectField, IntegerField, SubmitField, ValidationError
from wtforms.validators import Required

class QuestionForm(Form):
    text = TextField("Your question:", validators = [Required("Please enter your question.")])
    submit = SubmitField("Send")

class AnswerForm(Form):
    text = StringField("Enter your answer:", validators=[Required()])
    question = IntegerField()
    submit = SubmitField('Submit')