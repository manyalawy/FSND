#----------------------------------------------------------------------------#
# Imports
#----------------------------------------------------------------------------#

import json
import dateutil.parser
import babel
from flask import Flask, render_template, request, Response, flash, redirect, url_for
from flask_moment import Moment
from flask_sqlalchemy import SQLAlchemy
import logging
from logging import Formatter, FileHandler
from flask_wtf import Form
from forms import *
from flask_migrate import Migrate
from datetime import date


#----------------------------------------------------------------------------#
# App Config.
#----------------------------------------------------------------------------#

app = Flask(__name__)
moment = Moment(app)
app.config.from_object('config')
db = SQLAlchemy(app)

# TODO: connect to a local postgresql database
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://youssef@localhost:5432/fayur'
db = SQLAlchemy(app)
migrate = Migrate(app, db)

#----------------------------------------------------------------------------#
# Models.
#----------------------------------------------------------------------------#

                 
class Show(db.Model):
  __tablename__ = 'show'
  id = db.Column(db.Integer, primary_key=True)
  artist_id = db.Column(db.Integer)
  artist_name = db.Column(db.String())
  venue_id = db.Column(db.Integer)
  venue_name = db.Column(db.String())
  date = db.Column(db.String())

class Venue(db.Model):
    __tablename__ = 'venue'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String)
    city = db.Column(db.String(120))
    state = db.Column(db.String(120))
    address = db.Column(db.String(120))
    genres = db.Column(db.String(120))
    phone = db.Column(db.String(120))
    image_link = db.Column(db.String(500))
    facebook_link = db.Column(db.String(120))
    genres = db.Column(db.ARRAY(db.String(120)))


    # TODO: implement any missing fields, as a database migration using Flask-Migrate


class Artist(db.Model):
    __tablename__ = 'artist'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String)
    city = db.Column(db.String(120))
    state = db.Column(db.String(120))
    phone = db.Column(db.String(120))
    genres = db.Column(db.ARRAY(db.String()))
    image_link = db.Column(db.String(500))
    facebook_link = db.Column(db.String(120))

# TODO: implement any missing fields, as a database migration using Flask-Migrate

# TODO Implement Show and Artist models, and complete all model relationships and properties, as a database migration.

#----------------------------------------------------------------------------#
# s.
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

@app.route('/venues') #done
def venues():
    data = Venue.query.all()
    return render_template('pages/venues.html', areas=data)


@app.route('/venues/search', methods=['POST']) #done
def search_venues():
    # TODO: implement search on artists with partial string search. Ensure it is case-insensitive.
    # seach for Hop should return "The Musical Hop".
    # search for "Music" should return "The Musical Hop" and "Park Square Live Music & Coffee"

    search_term = request.form.get("search_term")
    results = Venue.query.filter(Venue.name.ilike('%' + search_term + '%')).all()
    response = {
        "count": len(results),
        "data": results
    }
    return render_template('pages/search_venues.html', results=response, search_term=request.form.get('search_term', ''))


@app.route('/venues/<int:venue_id>')
def show_venue(venue_id):
    # shows the venue page with the given venue_id
    # TODO: replace with real venue data from the venues table, using venue_id
    venue = Venue.query.filter_by(id= venue_id).one()
    venue_shows = Show.query.filter_by(venue_id = venue_id).all()
    past_shows = []
    upcoming_shows = []
    today = datetime.now()
    d1 = today.strftime("%Y-%m-%d %H:%M:%S")
    
    for show in venue_shows:
        if(show.date<d1):
          past_shows.append(show)
        
        else:
            upcoming_shows.append(show)

    data1 = {
        "id": venue.id,
        "name": venue.name,
        "genres": venue.genres,
        "address": venue.address,
        "city": venue.city,
        "state": venue.state,
        "phone": venue.phone,
        "website": "https://www.themusicalhop.com",
        "facebook_link": venue.facebook_link,
        "seeking_talent": True,
        "seeking_description": "We are on the lookout for a local artist to play every two weeks. Please call us.",
        "image_link": "https://images.unsplash.com/photo-1543900694-133f37abaaa5?ixlib=rb-1.2.1&ixid=eyJhcHBfaWQiOjEyMDd9&auto=format&fit=crop&w=400&q=60",
        "past_shows": past_shows,
        "upcoming_shows": upcoming_shows,
        "past_shows_count": len(past_shows),
        "upcoming_shows_count": len(upcoming_shows),
    }
    
    return render_template('pages/show_venue.html', venue=data1)

#  Create Venue
#  ----------------------------------------------------------------


@app.route('/venues/create', methods=['GET'])
def create_venue_form():
    form = VenueForm()
    return render_template('forms/new_venue.html', form=form)


@app.route('/venues/create', methods=['POST']) #done
def create_venue_submission():
  print(request.form.getlist('genres'))

  nam = request.form.get('name')
  cit = request.form.get('city')
  stat = request.form.get('state')
  addres = request.form.get('address')
  phon = request.form.get('phone')
  facebook_lin = request.form.get('facebook_link')
  genre = request.form.getlist('genres')
  ven = Venue(name=nam, city=cit, state=stat, address=addres,
                phone=phon, facebook_link=facebook_lin, genres = genre)
  try:
    db.session.add(ven)
    db.session.commit()
    flash("Venue added successfully")
    
  except:
    flash("Error adding venue")
  finally:
    db.session.close()
  return redirect(url_for('index'))
 
    





@ app.route('/venues/<venue_id>', methods=['DELETE'])
def delete_venue(venue_id):
    # TODO: Complete this endpoint for taking a venue_id, and using
    # SQLAlchemy ORM to delete a record. Handle cases where the session commit could fail.
    deleted_veneu = Venue.query.filter_by(id=venue_id).one()
    db.session.delete(delete_venue)
    db.session.commit()



    # BONUS CHALLENGE: Implement a button to delete a Venue on a Venue Page, have it so that
    # clicking that button delete it from the db then redirect the user to the homepage
    return redirect(url_for("venues"))

#  Artists
#  ----------------------------------------------------------------


@ app.route('/artists')
def artists():
    # TODO: replace with real data returned from querying the database
    artists =Artist.query.all()
    data = artists
    return render_template('pages/artists.html', artists=data)


@ app.route('/artists/search', methods=['POST'])
def search_artists():
    # TODO: implement search on artists with partial string search. Ensure it is case-insensitive.
    # seach for "A" should return "Guns N Petals", "Matt Quevado", and "The Wild Sax Band".
    # search for "band" should return "The Wild Sax Band".
    # artists = Artist.query.filter_by(Artist.name.)
    search_term = request.form.get("search_term")
    results = Artist.query.filter(Artist.name.ilike('%' + search_term + '%')).all()

    response={
        "count": len(results),
        "data": results
    }
    return render_template('pages/search_artists.html', results=response, search_term=request.form.get('search_term', ''))


@ app.route('/artists/<int:artist_id>')
def show_artist(artist_id):
    # shows the venue page with the given venue_id
    # TODO: replace with real venue data from the venues table, using venue_id
    artist = Artist.query.filter_by(id= artist_id).one()
    artist_shows = Show.query.filter_by(artist_id = artist_id).all()
    past_shows = []
    upcoming_shows = []
    today = datetime.now()
    d1 = today.strftime("%Y-%m-%d %H:%M:%S")
    
    for show in artist_shows:
        if(show.date<d1):
          past_shows.append(show)
        
        else:
            upcoming_shows.append(show)
        
        
    data1={
        "id": artist.id,
        "name": artist.name,
        "genres": artist.genres,
        "city": artist.city,
        "state": artist.state,
        "phone": artist.phone,
        "website": "https://www.gunsnpetalsband.com",
        "facebook_link": artist.facebook_link,
        "seeking_venue": True,
        "seeking_description": "Looking for shows to perform at in the San Francisco Bay Area!",
        "image_link": "https://images.unsplash.com/photo-1549213783-8284d0336c4f?ixlib=rb-1.2.1&ixid=eyJhcHBfaWQiOjEyMDd9&auto=format&fit=crop&w=300&q=80",
        "past_shows": past_shows,
        "upcoming_shows": upcoming_shows,
        "past_shows_count": len(past_shows),
        "upcoming_shows_count": len(upcoming_shows),
    }

    # data=list(filter(lambda d: d['id'] ==
    #                    artist_id, [data1, data2, data3]))[0]
    return render_template('pages/show_artist.html', artist=data1)

#  Update
#  ----------------------------------------------------------------


@ app.route('/artists/<int:artist_id>/edit', methods=['GET'])
def edit_artist(artist_id):
    form=ArtistForm()
    artist={
        "id": 4,
        "name": "Guns N Petals",
        "genres": ["Rock n Roll"],
        "city": "San Francisco",
        "state": "CA",
        "phone": "326-123-5000",
        "website": "https://www.gunsnpetalsband.com",
        "facebook_link": "https://www.facebook.com/GunsNPetals",
        "seeking_venue": True,
        "seeking_description": "Looking for shows to perform at in the San Francisco Bay Area!",
        "image_link": "https://images.unsplash.com/photo-1549213783-8284d0336c4f?ixlib=rb-1.2.1&ixid=eyJhcHBfaWQiOjEyMDd9&auto=format&fit=crop&w=300&q=80"
    }
    # TODO: populate form with fields from artist with ID <artist_id>
    return render_template('forms/edit_artist.html', form=form, artist=artist)


@ app.route('/artists/<int:artist_id>/edit', methods=['POST'])
def edit_artist_submission(artist_id):
    # TODO: take values from the form submitted, and update existing
    # artist record with ID <artist_id> using the new attributes

    return redirect(url_for('show_artist', artist_id=artist_id))


@ app.route('/venues/<int:venue_id>/edit', methods=['GET'])
def edit_venue(venue_id):
    form=VenueForm()
    venue={
        "id": 1,
        "name": "The Musical Hop",
        "genres": ["Jazz", "Reggae", "Swing", "Classical", "Folk"],
        "address": "1015 Folsom Street",
        "city": "San Francisco",
        "state": "CA",
        "phone": "123-123-1234",
        "website": "https://www.themusicalhop.com",
        "facebook_link": "https://www.facebook.com/TheMusicalHop",
        "seeking_talent": True,
        "seeking_description": "We are on the lookout for a local artist to play every two weeks. Please call us.",
        "image_link": "https://images.unsplash.com/photo-1543900694-133f37abaaa5?ixlib=rb-1.2.1&ixid=eyJhcHBfaWQiOjEyMDd9&auto=format&fit=crop&w=400&q=60"
    }
    # TODO: populate form with values from venue with ID <venue_id>
    return render_template('forms/edit_venue.html', form=form, venue=venue)


@ app.route('/venues/<int:venue_id>/edit', methods=['POST'])
def edit_venue_submission(venue_id):
    # TODO: take values from the form submitted, and update existing
    # venue record with ID <venue_id> using the new attributes
    return redirect(url_for('show_venue', venue_id=venue_id))

#  Create Artist
#  ----------------------------------------------------------------


@ app.route('/artists/create', methods=['GET']) #done
def create_artist_form():
    form=ArtistForm()
    return render_template('forms/new_artist.html', form=form)


@ app.route('/artists/create', methods=['POST']) #done
def create_artist_submission():
  name = request.form.get('name')
  city = request.form.get('city')
  phone = request.form.get('phone')
  genres = request.form.getlist('genres')
  facebook_link = request.form.get('facebook_link')
  artist = Artist(name= name, city = city, phone=phone, genres = genres, facebook_link = facebook_link)
  try:
    db.session.add(artist)
    db.session.commit()
    flash('Artist ' + name + ' was successfully listed!')
  except:
    flash('Artist not posted due to error')
  finally:
    db.session.close()
  return redirect(url_for('index'))
  
    
    # TODO: on unsuccessful db insert, flash an error instead.
    # e.g., flash('An error occurred. Artist ' + data.name + ' could not be listed.')
    # return render_template('pages/home.html')


#  Shows
#  ----------------------------------------------------------------

@ app.route('/shows')
def shows():
    # displays list of shows at /shows
    # TODO: replace with real venues data.
    #       num_shows should be aggregated based on number of upcoming shows per venue.
    data = Show.query.all()
    return render_template('pages/shows.html', shows=data)


@ app.route('/shows/create')
def create_shows():
    # renders form. do not touch.
    form=ShowForm()
    return render_template('forms/new_show.html', form=form)


@ app.route('/shows/create', methods=['POST']) 
def create_show_submission():
    # called to create new shows in the db, upon submitting new show listing form
    # TODO: insert form data as a new Show record in the db, instead
    
    

    try:
      artist = Artist.query.filter_by(id=request.form.get("artist_id")).all()
      venue = Venue.query.filter_by(id=request.form.get("venue_id")).all()
      if(len(artist)!=0 and len(venue)!=0):
        show = Show(artist_id=artist[0].id , artist_name=artist[0].name , venue_id = venue[0].id , venue_name= venue[0].name , date = request.form.get('start_time'))

        db.session.add(show)
        db.session.commit()
      
        flash("Show added")
      
      else:
        flash("Wrong id entered, please try again")
      
    except:
      flash("error")
    finally:
      db.session.close()
      return redirect(url_for('index'))
   
    
    db.session.add(artist)
    db.session.commit()
    # on successful db insert, flash success
    flash('Show was successfully listed!')
    # TODO: on unsuccessful db insert, flash an error instead.
    # e.g., flash('An error occurred. Show could not be listed.')
    # see: http://flask.pocoo.org/docs/1.0/patterns/flashing/
    return render_template('pages/home.html')


@ app.errorhandler(404)
def not_found_error(error):
    return render_template('errors/404.html'), 404


@ app.errorhandler(500)
def server_error(error):
    return render_template('errors/500.html'), 500


if not app.debug:
    file_handler=FileHandler('error.log')
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
