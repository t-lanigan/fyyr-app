#----------------------------------------------------------------------------#
# Imports
#----------------------------------------------------------------------------#

import json
import dateutil.parser
import babel
from flask import Flask, render_template, request, Response, flash, redirect, url_for, jsonify
import logging
from logging import Formatter, FileHandler
from flask_wtf import Form
from forms import *
from models import *


#----------------------------------------------------------------------------#
# Filters.
#----------------------------------------------------------------------------#


def format_datetime(value, format='medium'):
    date = dateutil.parser.parse(value)
    if format == 'full':
        format = "EEEE MMMM, d, y 'at' h:mma"
    elif format == 'medium':
        format = "EE MM, dd, y h:mma"
    return babel.dates.format_datetime(date, format)


app.jinja_env.filters['datetime'] = format_datetime

#----------------------------------------------------------------------------#
# Controllers.
#----------------------------------------------------------------------------#


@app.route('/')
def index():
    return render_template('pages/home.html')


#  Venues
#  ----------------------------------------------------------------

@app.route('/venues')
def venues():
    # TODO: replace with real venues data.
    #       num_shows should be aggregated based on number of upcoming shows per venue.
    data = []
    for value in db.session.query(Venue.city).distinct():
        venues = db.session.query(Venue).filter(
            Venue.city == value[0])
        d = {}
        d["city"] = value[0]
        d["state"] = venues.first().state
        d['venues'] = []
        for venue in venues:
            venues_dict = {}
            upcoming_shows = db.session.query(Show)\
                .filter_by(venue_id=venue.id)\
                .filter(Show.start_time > datetime.today())\
                .all()
            venues_dict['id'] = venue.id
            venues_dict['name'] = venue.name
            venues_dict['num_upcoming_shows'] = len(upcoming_shows)

            d['venues'].append(venues_dict)
        data.append(d)
    return render_template('pages/venues.html', areas=data)


@app.route('/venues/search', methods=['POST'])
def search_venues():
    wild_search_term = '%' + request.form.get('search_term', '') + '%'
    like_venues = Venue.query.filter(
        Venue.name.ilike(wild_search_term)).all()
    data = []
    for venue in like_venues:
        upcoming_shows = db.session.query(Show)\
            .filter_by(venue_id=venue.id)\
            .filter(Show.start_time > datetime.today())\
            .all()
        data.append(
            {
                "id": venue.id,
                "name": venue.name,
                "num_upcoming_shows": len(upcoming_shows)
            }
        )
    response = {
        "count": len(data),
        "data": data
    }
    return render_template('pages/search_venues.html', results=response, search_term=request.form.get('search_term', ''))


@app.route('/venues/<int:venue_id>')
def show_venue(venue_id):

    venue = Venue.query.filter_by(id=venue_id).first()
    data = venue.__dict__

    # Get the upcoming shows
    upcoming_shows = db.session.query(Show)\
        .filter_by(artist_id=venue_id)\
        .filter(Show.start_time > datetime.today())\
        .all()
    # Get the past shows:
    past_shows = db.session.query(Show)\
        .filter_by(artist_id=venue_id)\
        .filter(Show.start_time < datetime.today())\
        .all()

    data['past_shows'] = venue_show_data_helper(past_shows)
    data['upcoming_shows'] = venue_show_data_helper(upcoming_shows)
    data['past_shows_count'] = len(past_shows)
    data['upcoming_shows_count'] = len(upcoming_shows)

    return render_template('pages/show_venue.html', venue=data)


def venue_show_data_helper(shows):
    """Helper fuction for show_artist controller.
    """
    show_data = []
    for show in shows:
        d = {}
        d['artist_id'] = show.artist_id
        d['artist_name'] = show.artist.name
        d['artist_image_link'] = show.artist.image_link
        d['start_time'] = str(show.start_time)
        show_data.append(d)
    return show_data

    #  Create Venue
    #  ----------------------------------------------------------------


@app.route('/venues/create', methods=['GET'])
def create_venue_form():
    form = VenueForm()
    return render_template('forms/new_venue.html', form=form)


@app.route('/venues/create', methods=['POST'])
def create_venue_submission():
    form = VenueForm()
    try:
        venue = Venue(
            name=form.name.data,
            genres=form.genres.data,
            city=form.city.data,
            state=form.state.data,
            phone=form.phone.data,
            website=form.website.data,
            facebook_link=form.facebook_link.data,
            image_link=form.image_link.data,
            seeking_description=form.seeking_description.data,
            seeking_talent=form.seeking_talent.data
        )
        db.session.add(venue)
        db.session.commit()
        flash('Venue ' + request.form['name'] + ' was successfully listed!')
    except Exception as e:
        app.logger.error("An error occured: {}".format(e))
        flash('An error occurred. Venue ' +
              request.form['name'] + ' could not be listed.')
    return render_template('pages/home.html')


@app.route('/venues/<venue_id>', methods=['DELETE'])
def delete_venue(venue_id):
    try:
        # first we need to delete the shows
        shows = db.session.query(Show).filter_by(venue_id=venue_id).delete()

        # Now we can delete the venue.
        venue = db.session.query(Venue).filter_by(id=venue_id).first()
        name = venue.name
        msg = 'Venue, ' + name + ' successfully deleted.'
        db.session.delete(venue)
        db.session.commit()
        app.logger.info(msg)
        flash(msg)
    except Exception as e:
        app.logger.error(e)
        db.session.rollback()
        flash('Something went wrong. Venue ID: {} could not be deleted. Did it exist?'.format(
            venue_id))
    return render_template('pages/home.html')


@app.route('/artists/<artist_id>', methods=['DELETE'])
def delete_artist(artist_id):
    try:
        # first we need to delete the show
        show = db.session.query(Show).filter_by(artist_id=artist_id).delete()

        # Now we can delete the artist.
        artist = db.session.query(Artist).filter_by(id=artist_id).first()
        name = artist.name
        db.session.delete(artist)
        db.session.commit()
        msg = 'Artist, ' + name + ' successfully deleted.'
        app.logger.info(msg)
        flash(msg)
    except Exception as e:
        app.logger.error(e)
        db.session.rollback()
        flash('Something went wrong. Artist ID: {} could not be deleted. Did it exist?'.format(
            artist_id))
    return render_template('pages/home.html')


#  Artists
#  ----------------------------------------------------------------
@app.route('/artists')
def artists():
    data = Artist.query.all()
    return render_template('pages/artists.html', artists=data)


@app.route('/artists/search', methods=['POST'])
def search_artists():
    wild_search_term = '%' + request.form.get('search_term', '') + '%'
    like_artists = Artist.query.filter(
        Artist.name.ilike(wild_search_term)).all()

    data = []
    for artist in like_artists:
        upcoming_shows = db.session.query(Show)\
            .filter_by(artist_id=artist.id)\
            .filter(Show.start_time > datetime.today())\
            .all()
        data.append(
            {
                "id": artist.id,
                "name": artist.name,
                "num_upcoming_shows": len(upcoming_shows)
            }
        )

    response = {
        "count": len(data),
        "data": data
    }

    return render_template('pages/search_artists.html', results=response, search_term=request.form.get('search_term', ''))


@app.route('/artists/<int:artist_id>')
def show_artist(artist_id):
    artist = Artist.query.filter_by(id=artist_id).first()
    data = artist.__dict__

    # Get the upcoming shows
    upcoming_shows = db.session.query(Show)\
        .filter_by(artist_id=artist_id)\
        .filter(Show.start_time > datetime.today())\
        .all()
    # Get the past shows:
    past_shows = db.session.query(Show)\
        .filter_by(artist_id=artist_id)\
        .filter(Show.start_time < datetime.today())\
        .all()

    data['past_shows'] = artist_show_data_helper(past_shows)
    data['upcoming_shows'] = artist_show_data_helper(upcoming_shows)
    data['past_shows_count'] = len(past_shows)
    data['upcoming_shows_count'] = len(upcoming_shows)

    return render_template('pages/show_artist.html', artist=data)


def artist_show_data_helper(shows):
    """
    Helper fuction for show_artist controller.
    """
    show_data = []
    for show in shows:
        d = {}
        d['venue_id'] = show.venue_id
        d['venue_name'] = show.venue.name
        d['venue_image_link'] = show.venue.image_link
        d['start_time'] = str(show.start_time)
        show_data.append(d)
    return show_data

#  Update
#  ----------------------------------------------------------------
@app.route('/artists/<int:artist_id>/edit', methods=['GET'])
def edit_artist(artist_id):
    # TODO: add button to edit on venue page
    form = ArtistForm()
    artist = Artist.query.filter_by(id=artist_id).first()

    return render_template('forms/edit_artist.html', form=form, artist=artist)


@app.route('/artists/<int:artist_id>/edit', methods=['POST'])
def edit_artist_submission(artist_id):
    artist = Artist.query.get(artist_id)
    form = ArtistForm()
    try:
        artist.name = form.name.data,
        artist.city = form.city.data,
        artist.state = form.state.data,
        artist.phone = form.phone.data,
        artist.image_link = form.image_link.data,
        artist.genres = form.genres.data
        artist.facebook_link = form.facebook_link.data,
        artist.website = form.website.data,
        artist.seeking_description = form.seeking_description.data,
        artist.seeking_talent = form.seeking_venue.data
        db.session.commit()
        flash('Artist ' + request.form['name'] + ' was successfully updated.')
    except Exception as e:
        app.logger.error(e)
        flash('Something went wrong. Artist ' +
              request.form['name'] + ' could not be updated.')
        db.session.rollback()
    finally:
        db.session.close()

    return redirect(url_for('show_artist', artist_id=artist_id))


@app.route('/venues/<int:venue_id>/edit', methods=['GET'])
def edit_venue(venue_id):
    # TODO: add button to edit on venue page
    form = VenueForm()
    venue = Venue.query.filter_by(id=venue_id).first()
    return render_template('forms/edit_venue.html', form=form, venue=venue)


@app.route('/venues/<int:venue_id>/edit', methods=['POST'])
def edit_venue_submission(venue_id):
    venue = Venue.query.get(venue_id)
    form = VenueForm()
    try:
        venue.name = form.name.data,
        venue.city = form.city.data,
        venue.state = form.state.data,
        venue.phone = form.phone.data,
        venue.image_link = form.image_link.data,
        venue.genres = form.genres.data
        venue.facebook_link = form.facebook_link.data,
        venue.website = form.website.data,
        venue.address = form.address.data,
        venue.seeking_description = form.seeking_description.data,
        venue.address = form.address.data,
        venue.seeking_talent = form.seeking_talent.data
        db.session.commit()
        flash('Venue ' + request.form['name'] + ' was successfully updated.')
    except Exception as e:
        app.logger.error(e)
        flash('Something went wrong. Venue ' +
              request.form['name'] + ' could not be updated.')
        db.session.rollback()
    finally:
        db.session.close()
        return redirect(url_for('show_venue', venue_id=venue_id))

#  Create Artist
#  ----------------------------------------------------------------


@app.route('/artists/create', methods=['GET'])
def create_artist_form():
    form = ArtistForm()
    return render_template('forms/new_artist.html', form=form)


@app.route('/artists/create', methods=['POST'])
def create_artist_submission():
    form = ArtistForm()
    try:
        artist = Artist(
            name=form.name.data,
            genres=form.genres.data,
            city=form.city.data,
            state=form.state.data,
            phone=form.phone.data,
            website=form.website.data,
            facebook_link=form.facebook_link.data,
            image_link=form.image_link.data,
            seeking_description=form.seeking_description.data,
            seeking_venue=form.seeking_venue.data
        )

        db.session.add(artist)
        db.session.commit()
        flash('Artist ' + request.form['name'] + ' was successfully listed!')
    except Exception as e:
        app.logger.error("An error occured: {}".format(e))
        flash('An error occurred. Artist ' +
              request.form['name'] + ' could not be listed.')

    return render_template('pages/home.html')


#  Shows
#  ----------------------------------------------------------------

@app.route('/shows')
def shows():
    # displays list of shows at /shows
    data = []
    # Should be able to just db.session.query(Show).all(), but the front end
    # expects variable names like venue_name instead of venue.name. So we unpack here.
    for result in db.session.query(Show).all():
        data.append({
            "venue_id": result.venue_id,
            "venue_name": result.venue.name,
            "artist_id": result.artist_id,
            "artist_name": result.artist.name,
            "artist_image_link": result.artist.image_link,
            "start_time": str(result.start_time)
        })
    return render_template('pages/shows.html', shows=data)


@app.route('/shows/create')
def create_shows():
    # renders form. do not touch.
    form = ShowForm()
    return render_template('forms/new_show.html', form=form)


@app.route('/shows/create', methods=['POST'])
def create_show_submission():
    form = ShowForm()
    try:
        show = Show(
            artist_id=form.artist_id.data,
            venue_id=form.venue_id.data,
            start_time=form.start_time.data
        )
        db.session.add(show)
        db.session.commit()
        flash('Show successfully listed.')
    except:
        flash('Something went wrong. The show could not be listed.')
    return render_template('pages/home.html')


@app.errorhandler(404)
def not_found_error(error):
    return render_template('errors/404.html'), 404


@app.errorhandler(500)
def server_error(error):
    return render_template('errors/500.html'), 500


if not app.debug:
    file_handler = FileHandler('error.log')
    file_handler.setFormatter(
        Formatter(
            '%(asctime)s %(levelname)s: %(message)s [in %(pathname)s:%(lineno)d]')
    )
    app.logger.setLevel(logging.INFO)
    file_handler.setLevel(logging.INFO)
    app.logger.addHandler(file_handler)
    app.logger.info('errors')

#----------------------------------------------------------------------------#
# Launch.
#----------------------------------------------------------------------------#

# Default port:
if __name__ == '__main__':
    app.run()

# Or specify port manually:
'''
if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port)
'''
