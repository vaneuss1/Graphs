from flask import Flask, render_template, request, redirect, url_for
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import select


app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://postgres:Vanes991414@localhost/postgres'
db = SQLAlchemy(app)


class Annotator(db.Model):
    __tablename__ = 'Annotators'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String())
    surname = db.Column(db.String())
    tg_nickname = db.Column(db.String())
    project = db.Column(db.String())
    status = db.Column(db.String())
    manager = db.Column(db.String())

    def __init__(self, name, surname, tg_nickname, project, status, manager):
        self.name = name
        self.surname = surname
        self.tg_nickname = tg_nickname
        self.project = project
        self.status = status
        self.manager = manager


with app.app_context():
    db.create_all()


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/annotator/<id>/edit')
def edit_annotator(id):
    return render_template('edit_annotator.html', id=id)


@app.route('/annotator/<id>/remove')
def remove_annotator(id):
    Annotator.query.filter_by(id=id).delete()
    return redirect(url_for('annotators'))
@app.route('/add_annotator', methods=['GET', 'POST'])
def add_annotator():
    if request.method == 'POST':
        name = request.form.get('name')
        surname = request.form.get('surname')
        tg_nick = request.form.get('tg_nick')
        project = request.form.get('project')
        status = request.form.get('status')
        db.session.add(Annotator(name, surname, tg_nick, project, status, 'Семенов Иван'))
        db.session.commit()
        return redirect(url_for('annotators'))

    return render_template('add_annotator.html')

@app.route('/annotators')
def annotators():
    users = Annotator.query.all()
    return render_template('annotators.html', annotators=users)



app.run(debug=True)
