from werkzeug.security import generate_password_hash, check_password_hash
import jwt
from datetime import date
from flask import current_app
from datetime import datetime, timedelta
from app import db

rsvps = db.Table('rsvps',
	db.Column('user_id', db.Integer, db.ForeignKey('users.id')),
	db.Column('event_id', db.Integer, db.ForeignKey('events.id'))
	)
 
    ### defines the user data model###
class User(db.Model):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(64), unique=True)
    email = db.Column(db.String(64), unique=True)
    password_hash = db.Column(db.String(128))
    myrsvps = db.relationship('Events',
            secondary=rsvps,
            backref=db.backref('rsvps', lazy='dynamic'),
            lazy='dynamic')

    
    def password(self):
        raise AttributeError('password is not a readable attribute')

    @password.setter
    def password(self, password):
        self.password_hash = generate_password_hash(password)

    def verify_password(self, password):
        return check_password_hash(self.password_hash, password)

    def save(self):
        ###we will add user instance to session and save to databas###
        db.session.add(self)
        db.session.commit()

    
    def __repr__(self):
        return '<User %r>' % self.username



##events table##
class Events(db.Model):

    __tablename__ = 'events'
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'))
    name = db.Column(db.String(64))
    description = db.Column(db.Text)
    category = db.Column(db.String(64))
    location = db.Column(db.String(64))
    event_date = db.Column(db.DateTime)
    date_created = db.Column(db.DateTime, default=datetime.utcnow)
    
     ###this supposed to add a user to the list of rsvps###
    def add_rsvp(self, user):
        if not self.has_rsvp(user):
            self.rsvps.append(user)
            self.save()
            return "rsvp success"
        return "already registered"


        ###this is basically checking if a user is already registered for an event###
    def has_rsvp(self, user):
        return self.rsvps.filter_by(
            id=user.id).first() is not None

      
       ###its just adding the instance to session and saving###
    def save(self):
        db.session.add(self)
        db.session.commit()

       
        ### to delete a particular event###

    def delete(self):
        db.session.delete(self)
        db.session.commit()

        
        ### it would convert a given event to json###

    def to_json(self):
        json_event ={
            "id" : self.id,
            "name" : self.name,
            "description" : self.description,
            "category" : self.category,
            "location" : self.location,
            "orgarniser" : self.created_by.username,
            "event date" : self.event_date,
            "date created" : self.date_created
            }
        return json_event

    
    ###get an event with the given id###
    def get_event_by_id(event_id):
        return Events.query.filter_by(id=event_id).first()

       #filter events by category#
    def get_events_by_category(category, page, per_page):
        return Events.query.filter(Events.category.ilike("%" + category + "%"))\
        .filter(cast(Events.event_date, Date) >=  date.today())\
        .order_by(Events.event_date.desc()).paginate(page, per_page, error_out=False)


        ###filter events by location###
    def get_events_by_location(location, page, per_page):
        return Events.query.filter(Events.location.ilike("%" + location + "%"))\
        .filter(cast(Events.event_date, Date) >=  date.today())\
        .order_by(Events.event_date.desc())\
        .paginate(page, per_page, error_out=False)


 ###filter events by both category and location###
    def filter_events(location, category, page, per_page):    
        return Events.query.filter(Events.location.ilike("%" + location + "%"))\
                 .filter(Events.category.ilike("%" + category + "%"))\
                .filter(cast(Events.event_date, Date) >=  date.today())\
                .order_by(Events.event_date.desc())\
                .paginate(page, per_page, error_out=False)

    
     ###options filter events by name###
    def get_events_by_name(name, page, per_page):
       return Events.query.filter(Events.name.ilike("%" + name + "%"))\
        .order_by(Events.event_date.desc()).paginate(page, per_page, error_out=False)

    

    def __repr__(self):
        return '<Events %r>' % self.name


