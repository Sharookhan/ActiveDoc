from flask import Flask, render_template, request, redirect, url_for
from flask_sqlalchemy import SQLAlchemy
from hashlib import sha256

app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://root:root@localhost:3306/activedoc'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)
db.init_app(app)

from models import userdetails

@app.route('/')
def root():
    return render_template('index.html')


@app.route('/signup')
def signup():
    return render_template('signup.html')


@app.route('/welcome')
def welcome():
    return "<h1>Welcome </h1>"


@app.route('/', methods=['GET', 'POST'])
def login():
    error = None
    if request.method == 'POST':
        username = request.form.get("username")
        password = request.form.get("password")
        exists=None
        exists = db.session.query(db.engine.execute('select * from userdetails where username='+username+' AND password='+sha256(password.encode()).hexdigest()).exists()).scalar()
        if exists != True:
            error = 'Invalid Username or Password'
        else:
            return redirect(url_for('welcome'))
    return render_template('index.html', error=error)


@app.route('/signup', methods=['GET', 'POST'])
def register():
    error = None
    if request.method == 'POST':
        username = request.form.get("username")
        name = request.form.get("name")
        email = request.form.get("email")
        password = request.form.get("password")
        confirmpassword = request.form.get("cpassword")
        if password != confirmpassword:
            error = 'Passwords not Matching'
        else:
            exists = db.session.query(db.session.query(userdetails).filter_by(username=username).exists()).scalar()
            if exists == True:
                error = 'Username already Exit'
                exists = db.session.query(db.session.query(userdetails).filter_by(email=email).exists()).scalar()
            elif exists == True:
                error = 'Email id already Exit'
            else:
                new_user = userdetails(username, name, email, sha256(password.encode()).hexdigest())
                db.session.add(new_user)
                db.session.commit()
                return redirect(url_for('root'))

    return render_template('signup.html', error=error)
