class User(db.Model):
   id = db.Column(db.Integer, primary_key=True)
   username = db.Column(db.String(80), unique=True, nullable=False)
   password = db.Column(db.String(20), nullable=False)
   email = db.Column(db.String(100), unique=True, nullable=False)

   def __init__(self, username, password, email, country, city):
       self.username = username
       self.password = password
       self.email = email
       self.country= country
       self.city = city

   def __repr__(self):
       return '<User %r>' % self.username