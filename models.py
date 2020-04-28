from flask import Flask
from flask_moment import Moment
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate

#----------------------------------------------------------------------------#
# App Config.
#----------------------------------------------------------------------------#
app = Flask(__name__)
app.config.from_object('config')
moment = Moment(app)
db = SQLAlchemy(app)
# Hook flask db migrate up to the app
migrate = Migrate(app, db)


class CommonModel(db.Model):
    __abstract__ = True

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(120), unique=True)
    # Works for postsgres, but not everything.
    genres = db.Column(db.ARRAY(db.String()))
    city = db.Column(db.String(120))
    state = db.Column(db.String(120))
    phone = db.Column(db.String(120))
    website = db.Column(db.String(200))
    facebook_link = db.Column(db.String(120))
    seeking_description = db.Column(db.String(120))
    image_link = db.Column(db.String(500))


class Venue(CommonModel):
    __tablename__ = 'venues'

    address = db.Column(db.String(120))
    seeking_talent = db.Column(db.Boolean)
    shows = db.relationship('Show', backref='venue', lazy=True)

    def __repr__(self):
        return f'<Venue ID: {self.id} Name: {self.name}>'


class Artist(CommonModel):
    __tablename__ = 'artists'

    seeking_venue = db.Column(db.Boolean)
    shows = db.relationship('Show', backref='artist', lazy=True)

    def __repr__(self):
        return f'<Artist ID: {self.id} Name: {self.name}>'


class Show(db.Model):
    __tablename__ = 'shows'

    id = db.Column(db.Integer, primary_key=True)
    start_time = db.Column(db.DateTime, nullable=False)
    artist_id = db.Column(db.Integer, db.ForeignKey(
        'artists.id'), nullable=False)
    venue_id = db.Column(db.Integer, db.ForeignKey(
        'venues.id'), nullable=False)

    def __repr__(self):
        return f'<Show ID: {self.id} Start Time: {self.start_time}>'
