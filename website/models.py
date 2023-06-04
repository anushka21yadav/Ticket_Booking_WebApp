from . import db
from flask_login import UserMixin #usermixin ni pta

class User(db.Model, UserMixin):
    user_id = db.Column(db.Integer, primary_key=True)
    user_name = db.Column(db.String(150))
    user_email = db.Column(db.String(150), unique=True)
    user_password = db.Column(db.String(150))
    def get_id(self):
        return (self.user_id)  

class Admin(db.Model, UserMixin):
    admin_id = db.Column(db.Integer, primary_key=True)
    admin_name = db.Column(db.String(150))
    admin_email = db.Column(db.String(150), unique=True)
    admin_password = db.Column(db.String(150))
    def get_id(self):
        return (self.admin_id)

class Movies(db.Model):
    movie_id = db.Column(db.Integer, primary_key=True)    
    movie_name = db.Column(db.String(150))
    movie_venue = db.Column(db.String(150))
    movie_price = db.Column(db.Integer)
    movie_tags = db.Column(db.String(150))
    movie_capacity = db.Column(db.Integer) 
    avg_rating_s = db.Column(db.Integer, default = 2)

class Venue(db.Model):
    venue_id = db.Column(db.Integer, primary_key=True)
    venue_name = db.Column(db.String(150))
    venue_place = db.Column(db.String(150))
    venue_location = db.Column(db.String(150))
    avg_rating_v = db.Column(db.Integer, default = 2)

class Booking(db.Model):
    booking_id = db.Column(db.Integer, primary_key=True)
    booking_user = db.Column(db.String(150))
    booking_movie_name = db.Column(db.String(150))
    booking_venue = db.Column(db.String(150))
    booking_time = db.Column(db.String(150))
    booking_seats = db.Column(db.Integer)
    booking_cost = db.Column(db.Integer)   
    booking_rateing_s = db.Column(db.Integer, default = 2) 
    booking_rateing_v = db.Column(db.Integer, default = 2)

