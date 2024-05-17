from flask import Flask, redirect, url_for, render_template, request, session
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['SECRET_KEY'] = 'register'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///books.sqlite'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)


class Movies(db.Model):
    __tablename__ = 'movies'
    
    id = db.Column(db.Integer, primary_key=True)
    movie_title = db.Column(db.String(40), nullable=False)
    director = db.Column(db.String(30), nullable=False)
    rating = db.Column(db.Float, nullable=False)
    release_date = db.Column(db.String, nullable=False)


    def __str__(self):
        return f'Title of the movie:{self.title}; The director: {self.director}; The release date: {self.release_date}; The rating: {self.rating}'


class Accounts(db.Model):
    _tablename_ = 'accounts'
    
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String, nullable=False, unique=True)
    password = db.Column(db.String, nullable=False)
    creation_date = db.Column(db.String, nullable=False, default=str(datetime.utcnow()))

    def __str__(self):
        return f'Username: {self.username}; Password: {self.password}; Creation date: {self.creation_date}'333

# Calls db.create_all() in order to initialize all of the tables we created.
with app.app_context():
    db.create_all()
   

@app.route('/')
def home():
    return render_template('login.html')


@app.route('/login', methods=['POST', 'GET'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        session['user'] = username
        return redirect(url_for('user'))
    return render_template('login.html')



@app.route('/user')
def user():
    subjects = ['Python', 'Calculus', 'DB']
    return render_template('user.html',  subjects=subjects)


@app.route('/<name>/<age>')
def userage(name, age):
    return f'Hello {name}, your age is {age}'

@app.route('/logout')
def logout():
    session.pop('user', None)
    return 'You are logged out.'


@app.route('/books', methods=['GET', 'POST'])
def books():
    if request.method=='POST':
        title = request.form['title']
        director = request.form['director']
        releasedate = request.form['releasedate']
        rating = request.form['rating']
        movie1 = Movies(movie_title = title, director = director, release_date = releasedate, rating = rating)
        db.session.add(movie1)
        db.session.commit()
        return 'movie successfully added.'

    return render_template('books.html')

@app.route('/register', methods=['POST', 'GET'])
def register():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        if Accounts.query.filter_by(username=username).first():
            return 'Username already exists'
        new_user = Accounts(username=username, password=password, creation_date=str(datetime.utcnow()))
        db.session.add(new_user)
        db.session.commit()
        return redirect(url_for('login'))
    return render_template('register.html')

if __name__ == "__main__":
    app.run(debug=True)
  

