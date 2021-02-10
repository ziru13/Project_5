import forms
import models

from flask import Flask, g, redirect, url_for, render_template, flash, request, session

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
    g.db.session.commit()
    g.db.close()
    return response


@app.route('/')
def index():
    entries = models.Journal.select()
    return render_template('index.html', entries=entries)


@app.route('/detail/<int:entry_id>/update', methods=['GET', 'POST'])
def update(entry_id):
    """edit a journal entry."""
    entry = models.Journal.select().where(
        models.Journal.id == entry_id).get()
    form = forms.JournalForm()     # if the form validates
    if form.validate_on_submit():  # if click update button
        entry.title = form.title.data
        entry.date = form.date.data
        entry.time_spent = form.time_spent.data
        entry.learnt = form.learnt.data
        entry.resources = form.resources.data
        entry.save()  # commit the changes
        flash('Entry has been updated', 'success')
        return redirect(url_for('detail', entry_id=entry.id))
    elif request.method == 'GET':  # fill the form with current data
        form.title.data = entry.title
        form.date.data = entry.date
        form.time_spent.data = entry.time_spent
        form.learnt.data = entry.learnt
        form.resources.data = entry.resources
    return render_template('update.html', form=form)


@app.route('/detail/<int:entry_id>')
def detail(entry_id):
    entries = models.Journal.select().where(
        models.Journal.id == entry_id)
    return render_template('detail.html', entries=entries)


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


@app.route('/delete/<int:entry_id>', methods=['GET', 'POST'])
def delete(entry_id):
    entry = models.Journal.select().where(
        models.Journal.id == entry_id).get()
    entry.delete_instance()
    if entry.DoesNotExist:
        flash('Entry has been deleted!', 'success')
    return redirect(url_for('index'))


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
