from flask import Flask, render_template
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///db.sqlite'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)


class Story(db.Model):
    """ DB object to store HN story info """
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String)
    summary = db.Column(db.Text)
    url = db.Column(db.String)


class Position(db.Model):
    """ Store list of story ids to be shown on front page """
    id = db.Column(db.Integer, primary_key=True)
    position = db.Column(db.Integer)


@app.route('/')
def index():
    """ Front page view """
    # Get stories
    query = db.session.query(Story).join(Position, Story.id == Position.id)
    stories = query.order_by(Position.position).all()

    return render_template('index.html', stories=stories)
