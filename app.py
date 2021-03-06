#----------------------------------------------------------------------------#
# Imports
#----------------------------------------------------------------------------#

import json
import dateutil.parser
import babel
from flask import (
  Flask, 
  render_template, 
  request, 
  Response, 
  flash, 
  redirect, 
  url_for
)
from flask_moment import Moment
from flask_sqlalchemy import SQLAlchemy
import logging
from logging import Formatter, FileHandler
from flask_wtf import Form
from forms import *
from flask_migrate import Migrate
import sys
from datetime import datetime
from models import Venue, Artist, Show, db

#----------------------------------------------------------------------------#
# App Config.
#----------------------------------------------------------------------------#

app = Flask(__name__)
moment = Moment(app)
app.config.from_object('config')
db.init_app(app)



# TODO: connect to a local postgresql database

migrate = Migrate(app, db)

#----------------------------------------------------------------------------#
# Filters.
#----------------------------------------------------------------------------#

def format_datetime(value, format='medium'):
  date = dateutil.parser.parse(value)
  if format == 'full':
      format="EEEE MMMM, d, y 'at' h:mma"
  elif format == 'medium':
      format="EE MM, dd, y h:mma"
  return  date #babel.dates.format_datetime(date, format)

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
  
  current_time = datetime.now()
  venue_list=[]
  
  venues = Venue.query.join(Show, isouter=True).order_by(Venue.id).all()
  for i in range(len(venues)):
    num_upcoming_shows = 0
    for q in range(len(venues[i].shows)):
      if venues[i].shows[q].start_time > current_time:
        num_upcoming_shows += 1
    if venue_list == []:
      venue_list.append({
        "city": venues[i].city,
        "state": venues[i].state,
        "venues": [{
          "id": venues[i].id,
          "name": venues[i].name,
          "num_upcoming_shows": num_upcoming_shows,
        }]
      })
    else: 
      insert = True
      for j in range(len(venue_list)):
        if venue_list[j]['city'] == venues[i].city:
          venue_list[j]['venues'].append({
            "id": venues[i].id,
            "name": venues[i].name,
            "num_upcoming_shows": num_upcoming_shows,
          })
          insert = False
      if insert:
        venue_list.append({
          "city": venues[i].city,
          "state": venues[i].state,
          "venues": [{
            "id": venues[i].id,
            "name": venues[i].name,
            "num_upcoming_shows": num_upcoming_shows,
          }]
        })

  # data=[{
  #   "city": "San Francisco",
  #   "state": "CA",
  #   "venues": [{
  #     "id": 1,
  #     "name": "The Musical Hop",
  #     "num_upcoming_shows": 0,
  #   }, {
  #     "id": 3,
  #     "name": "Park Square Live Music & Coffee",
  #     "num_upcoming_shows": 1,
  #   }]
  # }, {
  #   "city": "New York",
  #   "state": "NY",
  #   "venues": [{
  #     "id": 2,
  #     "name": "The Dueling Pianos Bar",
  #     "num_upcoming_shows": 0,
  #   }]
  # }]
  return render_template('pages/venues.html', areas=venue_list)#data)

@app.route('/venues/search', methods=['POST'])
def search_venues():
  # TODO: implement search on artists with partial string search. Ensure it is case-insensitive.
  # seach for Hop should return "The Musical Hop".
  # search for "Music" should return "The Musical Hop" and "Park Square Live Music & Coffee"
  
  search_term = request.form.get('search_term')
  venues = Venue.query.join(Show, isouter=True).filter(Venue.name.ilike('%' + search_term + '%')).all()
  data = []

  for i in range(len(venues)):
    num_upcoming_shows = 0
    for j in range(len(venues[i].shows)):
      num_upcoming_shows += 1
    data.append({
      "id": venues[i].id,
      "name": venues[i].name,
      "num_upcoming_shows": num_upcoming_shows
    })

  response = {
    "count": len(venues),
    "data": data
  }

  # response={
  #   "count": 1,
  #   "data": [{
  #     "id": 2,
  #     "name": "The Dueling Pianos Bar",
  #     "num_upcoming_shows": 0,
  #   }]
  # }
  return render_template('pages/search_venues.html', results=response, search_term=request.form.get('search_term', ''))

@app.route('/venues/<int:venue_id>')
def show_venue(venue_id):
  # shows the venue page with the given venue_id
  # TODO: replace with real venue data from the venues table, using venue_id
  
  current_time = datetime.now()
  venue_list=[]
  venues = Venue.query.join(Show, isouter=True).order_by(Venue.id).all()
  for i in range(len(venues)):
    upcoming_shows = []
    past_shows = []
    past_shows_count = 0
    upcoming_shows_count = 0
    for j in range(len(venues[i].shows)):
      if venues[i].shows[j].start_time > current_time:
        artist= Artist.query.get(venues[i].shows[j].artist_id)
        upcoming_shows.append({
          "artist_id": venues[i].shows[j].artist_id,
          "artist_name": artist.name,
          "artist_image_link": artist.image_link,
          "start_time": venues[i].shows[j].start_time.strftime("%m/%d/%Y, %H:%M:%S")
        })
        upcoming_shows_count += 1
      else:
        artist= Artist.query.get(venues[i].shows[j].artist_id)
        past_shows.append({
          "artist_id": venues[i].shows[j].artist_id,
          "artist_name": artist.name,
          "artist_image_link": artist.image_link,
          "start_time": venues[i].shows[j].start_time.strftime("%m/%d/%Y, %H:%M:%S")
        })
        past_shows_count += 1
    venue_list.append({
      "id": venues[i].id,
      "name": venues[i].name,
      "genres": "".join(venues[i].genres).strip("}").strip("{").split(','),
      "city": venues[i].city,
      "state": venues[i].state,
      "phone": venues[i].phone,
      "website": venues[i].website,
      "facebook_link": venues[i].facebook_link,
      "seeking_venue": venues[i].seeking_talent,
      "seeking_description": venues[i].seeking_description,
      "image_link": venues[i].image_link,
      "past_shows": past_shows,
      "upcoming_shows": upcoming_shows,
      "past_shows_count": past_shows_count,
      "upcoming_shows_count": upcoming_shows_count,
    })

  
  # data1={
  #   "id": 1,
  #   "name": "The Musical Hop",
  #   "genres": ["Jazz", "Reggae", "Swing", "Classical", "Folk"],
  #   "address": "1015 Folsom Street",
  #   "city": "San Francisco",
  #   "state": "CA",
  #   "phone": "123-123-1234",
  #   "website": "https://www.themusicalhop.com",
  #   "facebook_link": "https://www.facebook.com/TheMusicalHop",
  #   "seeking_talent": True,
  #   "seeking_description": "We are on the lookout for a local artist to play every two weeks. Please call us.",
  #   "image_link": "https://images.unsplash.com/photo-1543900694-133f37abaaa5?ixlib=rb-1.2.1&ixid=eyJhcHBfaWQiOjEyMDd9&auto=format&fit=crop&w=400&q=60",
  #   "past_shows": [{
  #     "artist_id": 4,
  #     "artist_name": "Guns N Petals",
  #     "artist_image_link": "https://images.unsplash.com/photo-1549213783-8284d0336c4f?ixlib=rb-1.2.1&ixid=eyJhcHBfaWQiOjEyMDd9&auto=format&fit=crop&w=300&q=80",
  #     "start_time": "2019-05-21T21:30:00.000Z"
  #   }],
  #   "upcoming_shows": [],
  #   "past_shows_count": 1,
  #   "upcoming_shows_count": 0,
  # }
  # data2={
  #   "id": 2,
  #   "name": "The Dueling Pianos Bar",
  #   "genres": ["Classical", "R&B", "Hip-Hop"],
  #   "address": "335 Delancey Street",
  #   "city": "New York",
  #   "state": "NY",
  #   "phone": "914-003-1132",
  #   "website": "https://www.theduelingpianos.com",
  #   "facebook_link": "https://www.facebook.com/theduelingpianos",
  #   "seeking_talent": False,
  #   "image_link": "https://images.unsplash.com/photo-1497032205916-ac775f0649ae?ixlib=rb-1.2.1&ixid=eyJhcHBfaWQiOjEyMDd9&auto=format&fit=crop&w=750&q=80",
  #   "past_shows": [],
  #   "upcoming_shows": [],
  #   "past_shows_count": 0,
  #   "upcoming_shows_count": 0,
  # }
  # data3={
  #   "id": 3,
  #   "name": "Park Square Live Music & Coffee",
  #   "genres": ["Rock n Roll", "Jazz", "Classical", "Folk"],
  #   "address": "34 Whiskey Moore Ave",
  #   "city": "San Francisco",
  #   "state": "CA",
  #   "phone": "415-000-1234",
  #   "website": "https://www.parksquarelivemusicandcoffee.com",
  #   "facebook_link": "https://www.facebook.com/ParkSquareLiveMusicAndCoffee",
  #   "seeking_talent": False,
  #   "image_link": "https://images.unsplash.com/photo-1485686531765-ba63b07845a7?ixlib=rb-1.2.1&ixid=eyJhcHBfaWQiOjEyMDd9&auto=format&fit=crop&w=747&q=80",
  #   "past_shows": [{
  #     "artist_id": 5,
  #     "artist_name": "Matt Quevedo",
  #     "artist_image_link": "https://images.unsplash.com/photo-1495223153807-b916f75de8c5?ixlib=rb-1.2.1&ixid=eyJhcHBfaWQiOjEyMDd9&auto=format&fit=crop&w=334&q=80",
  #     "start_time": "2019-06-15T23:00:00.000Z"
  #   }],
  #   "upcoming_shows": [{
  #     "artist_id": 6,
  #     "artist_name": "The Wild Sax Band",
  #     "artist_image_link": "https://images.unsplash.com/photo-1558369981-f9ca78462e61?ixlib=rb-1.2.1&ixid=eyJhcHBfaWQiOjEyMDd9&auto=format&fit=crop&w=794&q=80",
  #     "start_time": "2035-04-01T20:00:00.000Z"
  #   }, {
  #     "artist_id": 6,
  #     "artist_name": "The Wild Sax Band",
  #     "artist_image_link": "https://images.unsplash.com/photo-1558369981-f9ca78462e61?ixlib=rb-1.2.1&ixid=eyJhcHBfaWQiOjEyMDd9&auto=format&fit=crop&w=794&q=80",
  #     "start_time": "2035-04-08T20:00:00.000Z"
  #   }, {
  #     "artist_id": 6,
  #     "artist_name": "The Wild Sax Band",
  #     "artist_image_link": "https://images.unsplash.com/photo-1558369981-f9ca78462e61?ixlib=rb-1.2.1&ixid=eyJhcHBfaWQiOjEyMDd9&auto=format&fit=crop&w=794&q=80",
  #     "start_time": "2035-04-15T20:00:00.000Z"
  #   }],
  #   "past_shows_count": 1,
  #   "upcoming_shows_count": 1,
  # }
  data = list(filter(lambda d: d['id'] == venue_id, venue_list))[0]
  return render_template('pages/show_venue.html', venue=data)

#  Create Venue
#  ----------------------------------------------------------------

@app.route('/venues/create', methods=['GET'])
def create_venue_form():
  form = VenueForm()
  return render_template('forms/new_venue.html', form=form)

@app.route('/venues/create', methods=['POST'])
def create_venue_submission():
  # TODO: insert form data as a new Venue record in the db, instead
  # TODO: modify data to be the data object returned from db insertion

  error = False
  venue_info = VenueForm(request.form, meta={'csrf': False})
  if venue_info.validate():
    try:
      name = venue_info['name'].data
      genres = venue_info['genres'].data
      city = venue_info['city'].data
      state = venue_info['state'].data
      phone = venue_info['phone'].data
      website = venue_info['website'].data
      address= venue_info['address'].data
      facebook = venue_info['facebook_link'].data
      if venue_info['seeking_talent'].data == 'True':
        seeking_talent = True
      else:
        seeking_talent = False
      seeking_description = venue_info['seeking_description'].data
      image = venue_info['image_link'].data
      venue = Venue(name=name, genres=genres, city=city, state=state, phone=phone, address=address, website=website, facebook_link=facebook, seeking_talent=seeking_talent, seeking_description=seeking_description, image_link=image)
      print("hello")
      db.session.add(venue)
      db.session.commit()
    except:
      db.session.rollback()
      error = True
      print(sys.exc_info())
    finally:
      db.session.close()
  else:
    error = True

  if error==False: 
    # on successful db insert, flash success
    flash('Venue ' + request.form['name'] + ' was successfully listed!')
  else:
    # TODO: on unsuccessful db insert, flash an error instead.
    # e.g., flash('An error occurred. Venue ' + data.name + ' could not be listed.')
    # see: http://flask.pocoo.org/docs/1.0/patterns/flashing/
    for error in venue_info.errors:
      flash(error)
    flash('An error occurred. Venue ' + venue_info['name'].data + ' could not be listed.')
  
  return render_template('pages/home.html')

@app.route('/venues/<venue_id>', methods=['DELETE'])
def delete_venue(venue_id):
  # TODO: Complete this endpoint for taking a venue_id, and using
  # SQLAlchemy ORM to delete a record. Handle cases where the session commit could fail.
  
  error = False
  try:
    venue = Venue.query.get(venue_id)
    db.session.delete(venue)
    db.session.commit()
  except:
    db.session.rollback()
    error = True
    print(sys.exc_info())
  finally:
    db.session.close()
  if error==False:
    flash('Venue ' + venue.name + ' was successfully deleted!')
  else:
    flash('An error occurred. Venue ' + venue.name + ' could not be deleted.')

  # BONUS CHALLENGE: Implement a button to delete a Venue on a Venue Page, have it so that
  # clicking that button delete it from the db then redirect the user to the homepage
  return redirect(url_for('index'))##############################

#  Artists
#  ----------------------------------------------------------------
@app.route('/artists')
def artists():
  # TODO: replace with real data returned from querying the database
  artist_list=[]
  artists = Artist.query.all()
  for i in range(len(artists)):
    artist_list.append({
      "id": artists[i].id,
      "name": artists[i].name,
    })

  
  # data=[{
  #   "id": 4,
  #   "name": "Guns N Petals",
  # }, {
  #   "id": 5,
  #   "name": "Matt Quevedo",
  # }, {
  #   "id": 6,
  #   "name": "The Wild Sax Band",
  # }]
  return render_template('pages/artists.html', artists=artist_list)#data)

@app.route('/artists/search', methods=['POST'])
def search_artists():
  # TODO: implement search on artists with partial string search. Ensure it is case-insensitive.
  # seach for "A" should return "Guns N Petals", "Matt Quevado", and "The Wild Sax Band".
  # search for "band" should return "The Wild Sax Band".
  
  search_term = request.form.get('search_term')
  artists = Artist.query.join(Show, isouter=True).filter(Artist.name.ilike('%' + search_term + '%')).all()
  data = []

  for i in range(len(artists)):
    num_upcoming_shows = 0
    for j in range(len(artists[i].shows)):
      num_upcoming_shows += 1
    data.append({
      "id": artists[i].id,
      "name": artists[i].name,
      "num_upcoming_shows": num_upcoming_shows
    })

  response = {
    "count": len(artists),
    "data": data
  }
  
  # response={
  #   "count": 1,
  #   "data": [{
  #     "id": 4,
  #     "name": "Guns N Petals",
  #     "num_upcoming_shows": 0,
  #   }]
  # }
  return render_template('pages/search_artists.html', results=response, search_term=request.form.get('search_term', ''))

@app.route('/artists/<int:artist_id>')
def show_artist(artist_id):
  # shows the venue page with the given venue_id
  # TODO: replace with real venue data from the venues table, using venue_id
  
  current_time = datetime.now()
  artist_list=[]
  artists = Artist.query.join(Show, isouter=True).all()
  for i in range(len(artists)):
    upcoming_shows = []
    past_shows = []
    num_upcoming_shows = 0
    num_past_shows = 0
    for j in range(len(artists[i].shows)):
      if artists[i].shows[j].start_time > current_time:
        venue = Venue.query.get(artists[i].shows[j].venue_id)
        upcoming_shows.append({
          "venue_id": venue.id,
          "venue_name": venue.name,
          "venue_image_link": venue.image_link,
          "start_time": artists[i].shows[j].start_time.strftime("%m/%d/%Y, %H:%M:%S")
        })
        num_upcoming_shows += 1
      else:
        venue = Venue.query.get(artists[i].shows[j].venue_id)
        past_shows.append({
          "venue_id": venue.id,
          "venue_name": venue.name,
          "venue_image_link": venue.image_link,
          "start_time": artists[i].shows[j].start_time.strftime("%m/%d/%Y, %H:%M:%S")
        })
        num_past_shows += 1
    artist_list.append({
      "id": artists[i].id,
      "name": artists[i].name,
      "genres": "".join(artists[i].genres).strip("}").strip("{").split(','),
      "city": artists[i].city,
      "state": artists[i].state,
      "phone": artists[i].phone,
      "website": artists[i].website,
      "facebook_link": artists[i].facebook_link,
      "seeking_venue": artists[i].seeking_venue,
      "seeking_description": artists[i].seeking_description,
      "image_link": artists[i].image_link,
      "past_shows": past_shows,
      "upcoming_shows": upcoming_shows,
      "past_shows_count": num_past_shows,
      "upcoming_shows_count": num_upcoming_shows,
    })
  
  # data1={
  #   "id": 4,
  #   "name": "Guns N Petals",
  #   "genres": ["Rock n Roll"],
  #   "city": "San Francisco",
  #   "state": "CA",
  #   "phone": "326-123-5000",
  #   "website": "https://www.gunsnpetalsband.com",
  #   "facebook_link": "https://www.facebook.com/GunsNPetals",
  #   "seeking_venue": True,
  #   "seeking_description": "Looking for shows to perform at in the San Francisco Bay Area!",
  #   "image_link": "https://images.unsplash.com/photo-1549213783-8284d0336c4f?ixlib=rb-1.2.1&ixid=eyJhcHBfaWQiOjEyMDd9&auto=format&fit=crop&w=300&q=80",
  #   "past_shows": [{
  #     "venue_id": 1,
  #     "venue_name": "The Musical Hop",
  #     "venue_image_link": "https://images.unsplash.com/photo-1543900694-133f37abaaa5?ixlib=rb-1.2.1&ixid=eyJhcHBfaWQiOjEyMDd9&auto=format&fit=crop&w=400&q=60",
  #     "start_time": "2019-05-21T21:30:00.000Z"
  #   }],
  #   "upcoming_shows": [],
  #   "past_shows_count": 1,
  #   "upcoming_shows_count": 0,
  # }
  # data2={
  #   "id": 5,
  #   "name": "Matt Quevedo",
  #   "genres": ["Jazz"],
  #   "city": "New York",
  #   "state": "NY",
  #   "phone": "300-400-5000",
  #   "facebook_link": "https://www.facebook.com/mattquevedo923251523",
  #   "seeking_venue": False,
  #   "image_link": "https://images.unsplash.com/photo-1495223153807-b916f75de8c5?ixlib=rb-1.2.1&ixid=eyJhcHBfaWQiOjEyMDd9&auto=format&fit=crop&w=334&q=80",
  #   "past_shows": [{
  #     "venue_id": 3,
  #     "venue_name": "Park Square Live Music & Coffee",
  #     "venue_image_link": "https://images.unsplash.com/photo-1485686531765-ba63b07845a7?ixlib=rb-1.2.1&ixid=eyJhcHBfaWQiOjEyMDd9&auto=format&fit=crop&w=747&q=80",
  #     "start_time": "2019-06-15T23:00:00.000Z"
  #   }],
  #   "upcoming_shows": [],
  #   "past_shows_count": 1,
  #   "upcoming_shows_count": 0,
  # }
  # data3={
  #   "id": 6,
  #   "name": "The Wild Sax Band",
  #   "genres": ["Jazz", "Classical"],
  #   "city": "San Francisco",
  #   "state": "CA",
  #   "phone": "432-325-5432",
  #   "seeking_venue": False,
  #   "image_link": "https://images.unsplash.com/photo-1558369981-f9ca78462e61?ixlib=rb-1.2.1&ixid=eyJhcHBfaWQiOjEyMDd9&auto=format&fit=crop&w=794&q=80",
  #   "past_shows": [],
  #   "upcoming_shows": [{
  #     "venue_id": 3,
  #     "venue_name": "Park Square Live Music & Coffee",
  #     "venue_image_link": "https://images.unsplash.com/photo-1485686531765-ba63b07845a7?ixlib=rb-1.2.1&ixid=eyJhcHBfaWQiOjEyMDd9&auto=format&fit=crop&w=747&q=80",
  #     "start_time": "2035-04-01T20:00:00.000Z"
  #   }, {
  #     "venue_id": 3,
  #     "venue_name": "Park Square Live Music & Coffee",
  #     "venue_image_link": "https://images.unsplash.com/photo-1485686531765-ba63b07845a7?ixlib=rb-1.2.1&ixid=eyJhcHBfaWQiOjEyMDd9&auto=format&fit=crop&w=747&q=80",
  #     "start_time": "2035-04-08T20:00:00.000Z"
  #   }, {
  #     "venue_id": 3,
  #     "venue_name": "Park Square Live Music & Coffee",
  #     "venue_image_link": "https://images.unsplash.com/photo-1485686531765-ba63b07845a7?ixlib=rb-1.2.1&ixid=eyJhcHBfaWQiOjEyMDd9&auto=format&fit=crop&w=747&q=80",
  #     "start_time": "2035-04-15T20:00:00.000Z"
  #   }],
  #   "past_shows_count": 0,
  #   "upcoming_shows_count": 3,
  # }
  data = list(filter(lambda d: d['id'] == artist_id, artist_list))[0] #[data1, data2, data3]))[0]
  return render_template('pages/show_artist.html', artist=data)

#  Update
#  ----------------------------------------------------------------
@app.route('/artists/<int:artist_id>/edit', methods=['GET'])
def edit_artist(artist_id):
  artist = Artist.query.get(artist_id)
  form = ArtistForm(request.form, meta={'csrf': False})
  data={
    "id": artist.id,
    "name": artist.name,
    "genres": artist.genres,
    "city": artist.city,
    "state": artist.state,
    "phone": artist.phone,
    "website": artist.website,
    "facebook_link": artist.facebook_link,
    "seeking_venue": artist.seeking_venue,
    "seeking_description": artist.seeking_description,
    "image_link": artist.image_link
  }
  # TODO: populate form with fields from artist with ID <artist_id>
  return render_template('forms/edit_artist.html', form=form, artist=data)

@app.route('/artists/<int:artist_id>/edit', methods=['POST'])
def edit_artist_submission(artist_id):
  # TODO: take values from the form submitted, and update existing
  # artist record with ID <artist_id> using the new attributes
  error = False
  artist_info = ArtistForm(request.form, meta={'csrf': False})
  if artist_info.validate():
    try:
      name = artist_info['name'].data
      genres = artist_info['genres'].data
      city = artist_info['city'].data
      state = artist_info['state'].data
      phone = artist_info['phone'].data
      website = artist_info['website'].data
      facebook = artist_info['facebook_link'].data
      if artist_info['seeking_venue'].data == 'True':
        seeking_venue = True
      else:
        seeking_venue = False
      seeking_description = artist_info['seeking_description'].data
      image = artist_info['image_link'].data
      artist = Artist(name=name, genres=genres, city=city, state=state, phone=phone, website=website, facebook_link=facebook, seeking_venue=seeking_venue, seeking_description=seeking_description, image_link=image)
      db.session.commit()
    except:
      db.session.rollback()
      error = True
      print(sys.exc_info())
    finally:
      db.session.close()
  else:
    error = True

  if error==False:
    # on successful db insert, flash success
    flash('Artist ' + request.form['name'] + ' was successfully updated!')
  else:
    # TODO: on unsuccessful db insert, flash an error instead.
    # e.g., flash('An error occurred. Artist ' + data.name + ' could not be listed.')
    
    flash('An error occurred. Artist ' + artist.name + ' could not be updated.')
  return redirect(url_for('show_artist', artist_id=artist_id))

@app.route('/venues/<int:venue_id>/edit', methods=['GET'])
def edit_venue(venue_id):
  venue = Venue.query.get(venue_id)
  form = VenueForm(request.form, meta={'csrf': False})
  data={
    "id": venue.id,
    "name": venue.name,
    "genres": venue.genres,#["Classical"],#"".join(venue.genres).strip("}").strip("{").split(','),
    "address": venue.address,
    "city": venue.city,
    "state": venue.state,
    "phone": venue.phone,
    "website": venue.website,
    "facebook_link": venue.facebook_link,
    "seeking_talent": venue.seeking_talent,
    "seeking_description": venue.seeking_description,
    "image_link": venue.image_link
  }
  # TODO: populate form with values from venue with ID <venue_id>
  return render_template('forms/edit_venue.html', form=form, venue=data)

@app.route('/venues/<int:venue_id>/edit', methods=['POST'])
def edit_venue_submission(venue_id):
  # TODO: take values from the form submitted, and update existing
  # venue record with ID <venue_id> using the new attributes

  error = False
  venue_info = VenueForm(request.form, meta={'csrf': False})
  if venue_info.validate():
    try:
      name = venue_info['name'].data
      genres = venue_info['genres'].data
      city = venue_info['city'].data
      state = venue_info['state'].data
      phone = venue_info['phone'].data
      website = venue_info['website'].data
      facebook = venue_info['facebook_link'].data
      if venue_info['seeking_talent'].data == 'True':
        seeking_talent = True
      else:
        seeking_talent = False
      seeking_description = venue_info['seeking_description'].data
      image = venue_info['image_link'].data
      venue = Venue(name=name, genres=genres, city=city, state=state, phone=phone, website=website, facebook_link=facebook, seeking_talent=seeking_talent, seeking_description=seeking_description, image_link=image)
      db.session.commit()
    except:
      db.session.rollback()
      error = True
      print(sys.exc_info())
    finally:
      db.session.close()
  else:
    error = True

  if error==False: 
    # on successful db insert, flash success
    flash('Venue ' + request.form['name'] + ' was successfully updated!')
  else:
    # TODO: on unsuccessful db insert, flash an error instead.
    # e.g., flash('An error occurred. Venue ' + data.name + ' could not be listed.')
    # see: http://flask.pocoo.org/docs/1.0/patterns/flashing/
    for error in venue_info.errors:
      flash(error)
    flash('An error occurred. Venue ' + venue_info['name'].data + ' could not be updated.')
  
  return redirect(url_for('show_venue', venue_id=venue_id))

#  Create Artist
#  ----------------------------------------------------------------

@app.route('/artists/create', methods=['GET'])
def create_artist_form():
  form = ArtistForm()
  return render_template('forms/new_artist.html', form=form)

@app.route('/artists/create', methods=['POST'])
def create_artist_submission():
  # called upon submitting the new artist listing form
  # TODO: insert form data as a new Venue record in the db, instead
  # TODO: modify data to be the data object returned from db insertion
  error = False
  artist_info = ArtistForm(request.form, meta={'csrf': False})
  if artist_info.validate():
    try:
      name = artist_info['name'].data
      genres = artist_info['genres'].data
      city = artist_info['city'].data
      state = artist_info['state'].data
      phone = artist_info['phone'].data
      website = artist_info['website'].data
      facebook = artist_info['facebook_link'].data
      if artist_info['seeking_venue'].data == 'True':
        seeking_venue = True
      else:
        seeking_venue = False
      seeking_description = artist_info['seeking_description'].data
      image = artist_info['image_link'].data
      artist = Artist(name=name, genres=genres, city=city, state=state, phone=phone, website=website, facebook_link=facebook, seeking_venue=seeking_venue, seeking_description=seeking_description, image_link=image)
      db.session.add(artist)
      db.session.commit()
    except:
      db.session.rollback()
      error = True
      print(sys.exc_info())
    finally:
      db.session.close()
  else:
    error = True

  if error==False:
    # on successful db insert, flash success
    flash('Artist ' + request.form['name'] + ' was successfully listed!')
  else:
    # TODO: on unsuccessful db insert, flash an error instead.
    # e.g., flash('An error occurred. Artist ' + data.name + ' could not be listed.')
    flash('An error occurred. Artist ' + artist.name + ' could not be listed.')
  return render_template('pages/home.html')


#  Shows
#  ----------------------------------------------------------------

@app.route('/shows')
def shows():
  # displays list of shows at /shows
  # TODO: replace with real venues data.
  #       num_shows should be aggregated based on number of upcoming shows per venue.
  
  show_list=[]
  shows = Show.query.all()
  for i in range(len(shows)):
    show_list.append({
      "venue_id": shows[i].venue_id,
      "venue_name": shows[i].venue.name,
      "artist_id":shows[i].id,
      "artist_name": shows[i].artist.name,
      "artist_image_link": shows[i].artist.image_link,
      "start_time": shows[i].start_time.strftime("%m/%d/%Y, %H:%M:%S")
    })
  
  
  
  # data=[{
  #   "venue_id": 1,
  #   "venue_name": "The Musical Hop",
  #   "artist_id": 2,
  #   "artist_name": "Guns N Petals",
  #   "artist_image_link": "https://images.unsplash.com/photo-1549213783-8284d0336c4f?ixlib=rb-1.2.1&ixid=eyJhcHBfaWQiOjEyMDd9&auto=format&fit=crop&w=300&q=80",
  #   "start_time": "2019-05-21T21:30:00.000Z"
  # }, {
  #   "venue_id": 3,
  #   "venue_name": "Park Square Live Music & Coffee",
  #   "artist_id": 3,
  #   "artist_name": "Matt Quevedo",
  #   "artist_image_link": "https://images.unsplash.com/photo-1495223153807-b916f75de8c5?ixlib=rb-1.2.1&ixid=eyJhcHBfaWQiOjEyMDd9&auto=format&fit=crop&w=334&q=80",
  #   "start_time": "2019-06-15T23:00:00.000Z"
  # }, {
  #   "venue_id": 3,
  #   "venue_name": "Park Square Live Music & Coffee",
  #   "artist_id": 4,
  #   "artist_name": "The Wild Sax Band",
  #   "artist_image_link": "https://images.unsplash.com/photo-1558369981-f9ca78462e61?ixlib=rb-1.2.1&ixid=eyJhcHBfaWQiOjEyMDd9&auto=format&fit=crop&w=794&q=80",
  #   "start_time": "2035-04-01T20:00:00.000Z"
  # }, {
  #   "venue_id": 3,
  #   "venue_name": "Park Square Live Music & Coffee",
  #   "artist_id": 4,
  #   "artist_name": "The Wild Sax Band",
  #   "artist_image_link": "https://images.unsplash.com/photo-1558369981-f9ca78462e61?ixlib=rb-1.2.1&ixid=eyJhcHBfaWQiOjEyMDd9&auto=format&fit=crop&w=794&q=80",
  #   "start_time": "2035-04-08T20:00:00.000Z"
  # }, {
  #   "venue_id": 3,
  #   "venue_name": "Park Square Live Music & Coffee",
  #   "artist_id": 4,
  #   "artist_name": "The Wild Sax Band",
  #   "artist_image_link": "https://images.unsplash.com/photo-1558369981-f9ca78462e61?ixlib=rb-1.2.1&ixid=eyJhcHBfaWQiOjEyMDd9&auto=format&fit=crop&w=794&q=80",
  #   "start_time": "2035-04-15T20:00:00.000Z"
  # }]
  return render_template('pages/shows.html', shows=show_list)#data)

@app.route('/shows/create')
def create_shows():
  # renders form. do not touch.
  form = ShowForm()
  return render_template('forms/new_show.html', form=form)

@app.route('/shows/create', methods=['POST'])
def create_show_submission():
  # called to create new shows in the db, upon submitting new show listing form
  # TODO: insert form data as a new Show record in the db, instead
  error = False
  show_info = ShowForm(request.form)
  if show_info.validate():
    try:
      artist_id = show_info['artist_id'].data
      venue_id = show_info['venue_id'].data
      start_time = show_info['start_time'].data
      show = Show(artist_id=artist_id, venue_id=venue_id, start_time=start_time)
      db.session.add(show)
      db.session.commit()
    except:
      db.session.rollback()
      error = True
      print(sys.exc_info())
    finally:
      db.session.close()
  else:
    error = True

  if error==False:
    # on successful db insert, flash success
    flash('Show was successfully listed!')
  else:
    # TODO: on unsuccessful db insert, flash an error instead.
    # e.g., flash('An error occurred. Show could not be listed.')
    # see: http://flask.pocoo.org/docs/1.0/patterns/flashing/
    flash('An error occurred. Show could not be listed.')

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
        Formatter('%(asctime)s %(levelname)s: %(message)s [in %(pathname)s:%(lineno)d]')
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
