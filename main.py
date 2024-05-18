from flask import Flask, redirect, url_for, render_template, request, session
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

app = Flask(__name__)
app.config['SECRET_KEY'] = 'register'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///movies.sqlite'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

class Movies(db.Model):
    __tablename__ = 'movies'
    account_name=db.Column(db.String,nullable=False)
    id = db.Column(db.Integer, primary_key=True)
    movie_title = db.Column(db.String(40), nullable=False)
    director = db.Column(db.String(30), nullable=False)
    rating = db.Column(db.Float, nullable=False)
    release_date = db.Column(db.String, nullable=False)
    
    def __str__(self):
        return f'Title of the movie: {self.movie_title}; The director: {self.director}; The release date: {self.release_date}; The rating: {self.rating}'

class Accounts(db.Model):
    __tablename__ = 'accounts'

    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String, nullable=False, unique=True)
    password = db.Column(db.String, nullable=False)
    creation_date = db.Column(db.String, nullable=False, default=str(datetime.now()))

    def __str__(self):
        return f'Username: {self.username}; Password: {self.password}; Creation date: {self.creation_date}'

with app.app_context():
    db.create_all()

@app.route('/')
def home():
    return redirect(url_for('login'))

@app.route('/login', methods=['POST', 'GET'])
def login():
    '''The URL used for logging in. If the user inputs incorrect credentials, for now, it only returns a blank screen with: "invalid username or password"'''

    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        if Accounts.query.filter_by(username=username, password=password).first():
            session['user'] = username
            return redirect(url_for('user'))
        return 'Invalid username or password'
    return render_template('login.html')

@app.route('/user')
def user():
    '''This portrays the added movies. So far, this has no CSS but we will add it later.'''

    movies=Movies.query.filter_by(account_name=session['user']).all()
    return render_template('user.html', movies=movies)

@app.route('/logout')
def logout():
    session.pop('user', None)
    return redirect(url_for('login'))



@app.route('/movies', methods=['GET', 'POST'])
def movies():
    '''The user can add the movies on this page'''

    if request.method=='POST':
        title = request.form['title']
        director = request.form['director']
        releasedate = request.form['releasedate']
        rating = request.form['rating']
        movie1 = Movies(movie_title = title, director = director, release_date = releasedate, rating = rating, account_name=session['user'])
        db.session.add(movie1)
        db.session.commit()
        return 'Movie successfully added.'

    return render_template('movies.html')

@app.route('/register', methods=['POST', 'GET'])
def register():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        if Accounts.query.filter_by(username=username).first():
            return 'Username already exists'
        new_user = Accounts(username=username, password=password, creation_date=str(datetime.now()))
        db.session.add(new_user)
        db.session.commit()
        return redirect(url_for('login'))
    return render_template('register.html')

if __name__ == "__main__":
    app.run(debug=True)
