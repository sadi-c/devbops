

class Service(db.Model):
   id = db.Column(db.Integer, primary_key=True)
   content = db.Column(db.Text)
   add_date = db.Column(db.DateTime, default=datetime.datetime.now())
   end_date = db.Column(db.DateTime)
   done = db.Column(db.Boolean, default=False)
   user = db.relationship('User', backref='service', lazy=True)
   user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)

   def __init__(self, content, user):
       self.content = content
       self.user = user

   def __repr__(self):
       return '<Task %r>' % self.content