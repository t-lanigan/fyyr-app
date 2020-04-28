from app import Show, Artist, Venue
from datetime import datetime
from app import db


venue = Venue(
    name='The Fake Bar',
    genres=["Jazz", "Reggae", "Swing", "Classical", "Folk"],
    address='555 Fake Drive',
    city='Fakesville',
    state='CA',
    phone='555-555-5555',
    website='https://www.youtube.com/watch?v=dQw4w9WgXcQ',
    facebook_link='https://www.facebook.com/joeexotic',
    seeking_talent=True,
    seeking_description='Fake it till you make it baby!',
    image_link='https://images.unsplash.com/photo-1543900694-133f37abaaa5?ixlib=rb-1.2.1&ixid=eyJhcHBfaWQiOjEyMDd9&auto=format&fit=crop&w=400&q=60',
)
venue2 = Venue(
    name='The Faker Bar',
    genres=["Jazz", "Folk"],
    address='555 Faker Drive',
    city='Coolville',
    state='CA',
    phone='666-666-6666',
    website='https://www.youtube.com/watch?v=dQw4w9WgXcQ',
    facebook_link='https://www.facebook.com/joeexotic',
    seeking_talent=True,
    seeking_description='Noice!',
    image_link='https://images.unsplash.com/photo-1543900694-133f37abaaa5?ixlib=rb-1.2.1&ixid=eyJhcHBfaWQiOjEyMDd9&auto=format&fit=crop&w=400&q=60',
)

artist = Artist(
    name="Justin Beiberlake",
    genres=["Jazz", "Reggae", "Swing", "Classical", "Folk"],
    city='Fakesville',
    state="CA",
    phone='555-555-5556',
    website='https://www.youtube.com/watch?v=dQw4w9WgXcQ',
    facebook_link='https://www.facebook.com/joeexotic',
    image_link="https://images.unsplash.com/photo-1549213783-8284d0336c4f?ixlib=rb-1.2.1&ixid=eyJhcHBfaWQiOjEyMDd9&auto=format&fit=crop&w=300&q=80",
    seeking_venue=True,
    seeking_description='Fake it till you make it baby!'
)

artist2 = Artist(
    name="Chris Cornelton",
    genres=["Swing", "Classical", "Folk"],
    city='Fakesville',
    state="CA",
    phone='555-555-5456',
    website='https://www.youtube.com/watch?v=dQw4w9WgXcQ',
    facebook_link='https://www.facebook.com/joeexotic',
    image_link="https://images.unsplash.com/photo-1549213783-8284d0336c4f?ixlib=rb-1.2.1&ixid=eyJhcHBfaWQiOjEyMDd9&auto=format&fit=crop&w=300&q=80",
    seeking_venue=True,
    seeking_description='Fake it till you make it baby!'
)
add_list = [venue, venue2, artist, artist2]
[db.session.add(item) for item in add_list]
db.session.commit()

show = Show(
    start_time=datetime(2020, 4, 25, 20, 40, 19, 448277),
    artist_id=1,
    venue_id=1
)

show2 = Show(
    start_time=datetime(2020, 6, 25, 20, 40, 19, 448277),
    artist_id=2,
    venue_id=2
)

add_list = [show, show2]
[db.session.add(item) for item in add_list]
db.session.commit()

db.session.close()
