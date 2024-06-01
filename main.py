from flask import Flask, redirect, url_for, render_template, request, session
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
from movie_api import MovieFinder
from flask import flash

app = Flask(__name__)
app.config['SECRET_KEY'] = 'register'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///movies.sqlite'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)
api = MovieFinder()

class Movies(db.Model):
    __tablename__ = 'movies'
    account_name=db.Column(db.String,nullable=False)
    id = db.Column(db.Integer, primary_key=True)
    movie_title = db.Column(db.String(40), nullable=False)
    rating = db.Column(db.Float, nullable=False)
    release_date = db.Column(db.String, nullable=False)
    
    def __str__(self):
        return f'Title of the movie: {self.movie_title};  The release date: {self.release_date}; The rating: {self.rating}'

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
    try:
        if not session.get('user'):
            return redirect(url_for('login'))
        else:
            return redirect(url_for('user'))
    except Exception as e:
        flash(f'An error occurred: {e}')
        return render_template('error.html')


@app.route('/login/<langg>', methods=['POST', 'GET'])   
def login(langg):
        '''The login page. There is an option to change the language'''
        if request.method == 'POST':
            username = request.form['username']
            password = request.form['password']
            try:
                user = Accounts.query.filter_by(username=username, password=password).first()
                if user:
                    session['user'] = username
                    return redirect(url_for('user'))
                else:
                    flash('Invalid username or password')
                    return render_template('login.html', lang = langg)
            except Exception as e:
                flash(f'An error occurred: {e}')
                return render_template('login.html', lang = langg)
        return render_template('login.html', lang = langg)


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

    if request.method == 'POST':
        title = request.form['title']
        releasedate = request.form['releasedate']
        rating = request.form['rating']
        try:
            if not title or not releasedate or not rating:
                flash('All fields are required')
                return render_template('movies.html')
            movie1 = Movies(movie_title=title, release_date=releasedate, rating=rating, account_name=session['user'])
            db.session.add(movie1)
            db.session.commit()
            flash('Movie successfully added.')
            return render_template('movies.html')
        except Exception as e:
            flash(f'An error occurred: {e}')
            return render_template('movies.html')
    return render_template('movies.html')


@app.route('/register/<langg>', methods=['POST', 'GET'])
def register(langg):
    '''Just like the login page, changing the language is possible'''

    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        try:
            if not username or not password:
                flash('Username and password are required')
                return render_template('register.html')
            if Accounts.query.filter_by(username=username).first():
                flash('Username already exists')
                return render_template('register.html')
                 hashed_password = generate_password_hash(password, method='sha256')
                new_user = Accounts(username=username, password=password, creation_date=str(datetime.now()))
            db.session.add(new_user)
            db.session.commit()
            flash('Registration successful. Please log in.')
            return render_template('login.html')
        except Exception as e:
            flash(f'An error occurred: {e}')
            return render_template('register.html', lang = langg)
    return render_template('register.html', lang = langg)


@app.route('/recommendations', methods=['GET', 'POST'])
def recommendation_page():
    '''Utilizes the API module and gets the recommended movies based on user input.'''
    
    if request.method == 'POST':
        movie_name = request.form['moviename']
        try:
            data = api.search_func(movie_name)
            recommendations = api.parse_moviedata(data)
            return render_template('add_movies.html', recommendations=recommendations)
        except Exception as e:
            flash(f'An error occurred: {e}')
            return render_template('add_movies.html')
    return render_template('add_movies.html', recommendations=[])


if __name__ == "__main__":
    app.run(debug=True)
