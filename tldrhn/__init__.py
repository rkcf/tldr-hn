from flask import Flask, render_template, request, url_for
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
    # Get page request arg
    page = request.args.get('p', 1, type=int)

    # Get stories
    query = db.session.query(Story).join(Position, Story.id == Position.id)
    stories = query.order_by(Position.position).paginate(page, 10, False)

    # Generate pagination links
    if stories.has_next:
        next_page = url_for('index', p=stories.next_num)
    else:
        next_page = None
    if stories.has_prev:
        prev_page = url_for('index', p=stories.prev_num)
    else:
        prev_page = None

    return render_template('index.html',
                           stories=stories.items,
                           next_page=next_page,
                           prev_page=prev_page)
