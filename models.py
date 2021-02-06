# pip install flask-login
from flask_login import UserMixin
from peewee import *

DATABASE = SqliteDatabase('journals.db')


class Journal(Model):
    title = TextField()
    date = DateField()
    time_spent = CharField()
    learnt = TextField()
    resources = TextField()

    class Meta:
        database = DATABASE

    @classmethod
    def create_journal(cls, title, date, time_spent, learnt, resources):
        cls.create(
            title=title,
            date=date,
            time_spent=time_spent,
            learnt=learnt,
            resources=resources)


def initialize():
    DATABASE.connect()
    DATABASE.create_tables([Journal], safe=True)
    DATABASE.close()