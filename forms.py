from flask_wtf import Form  # pip install flask_wtf
from wtforms import StringField
from wtforms.validators import DataRequired


class JournalForm(Form):
    title = StringField(
        'Title Of Task',
        validators=[DataRequired()])

    date = StringField(
        'Date (DD/MM/YYYY)',
        validators=[DataRequired()])

    time_spent = StringField(
        'Time Spent',
        validators=[DataRequired()])

    learnt = StringField(
        'What You Learned',
        validators=[DataRequired()])

    resources = StringField(
        'Resources To Remember (Optional)',
        validators=[])
