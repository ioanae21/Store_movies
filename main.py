from flask import Flask, redirect, url_for, render_template, request, session
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['SECRET_KEY'] = 'register'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///books.sqlite'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)


class Movies(db.Model):
    '''Creating a template of the movies table.'''


    def __str__(self):
        return f'Title of the movie:{self.title}; The director: {self.director}; The release date: {self.release_date}; The rating: {self.rating}'




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
        b1 = Movies(title = 'blank', director = 'blank', release_date = 'blank', rating = 'blank')
        db.session.add(b1)
        db.session.commit()
        return ''

    return render_template('books.html')

@app.route('/register', methods = ['GET', 'POST'])
def register():
    return render_template('register.html')

if __name__ == "__main__":
    app.run(debug=True)