Import flask

##

@app.route('/signup', methods=['POST'])
def signup():
   username = request.form['username']
   password = request.form['password']
   email = request.form['email']
   country = request.form['country']
   city = request.form['city']
   user = User(username=username, password=password, email=email, country=country, city=city)
   db.session.add(user)
   db.session.commit()
   return jsonify({
       'response': 'User ' + username + ' created successfully'
   })