import forms
import models

from flask import Flask, g, redirect, url_for, render_template, flash

DEBUG = True
PORT = 8000
HOST = '127.0.0.1'

app = Flask(__name__)
app.secret_key = 'dsqweoriiuhgl;\[]pvxcm,1234454@#$%^&*(()_+?2dfweeewpo{}'


@app.before_request
def before_request():
    g.db = models.DATABASE
    g.db.connect()


@app.after_request
def after_request(response):
    g.db.close()
    return response


@app.route('/')
def index():
    entries = models.Journal.select()
    return render_template('index.html', entries=entries)


@app.route('/add', methods=['GET', 'POST'])
def add():
    """Create a journal entry."""
    form = forms.JournalForm()
    if form.validate_on_submit():
        models.Journal.create(
            title=form.title.data,
            date=form.date.data,
            time_spent=form.time_spent.data,
            learnt=form.learnt.data,
            resources=form.resources.data)
        flash('Entry has been created', 'success')
        return redirect(url_for('index'))
    return render_template('add.html', form=form)


@app.route('/details/<int:entry_id>')
def detail(entry_id):
    journals = models.Journal.select().where(
        models.Journal.id == entry_id)
    return render_template('detail.html', entries=journals)


@app.route('/delete/<int:entry_id>', methods=['GET', 'POST'])
def delete(entry_id):
    entry = models.Journal.select().where(
        models.Journal.id == entry_id).get()
    entry.delete_instance()
    if entry.DoesNotExist:
        flash('Entry has been deleted!', 'success')
    return redirect(url_for('index'))

# @app.route('/entries/edit/<int:entry_id>', methods=['GET', 'POST'])
# def edit(entry_id):
#     


if __name__ == '__main__':
    models.initialize()
    # try:
    #     models.Journal.create_journal(
    #             title='Project 5',
    #             date='2021/02/04',
    #             time_spent="3 days",
    #             learnt='Build a personal learning journal with Flask',
    #             resources="Flask"
    #         )
    # except ValueError:
    #     pass

    app.run(debug=DEBUG, host=HOST, port=PORT)