from flask import Flask, render_template, request, redirect, url_for, session, jsonify
from flask_sqlalchemy import SQLAlchemy
from hashlib import sha256
import random

app = Flask(__name__)
app.secret_key = 'Thisisthesecretkey'
app.config['SQLALCHEMY_DATABASE_URI'] = 'potgres://fntwhugnbcksel:eb206c4c5286a6a44e0cc300e10d9adbd0b110bbda3fcb1e142dd5376149d982@ec2-52-202-66-191.compute-1.amazonaws.com:5432/d8ef42tm3os6ai'
#app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://root:root@localhost:3306/activedoc'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)
db.init_app(app)

from models import userdetails,logindetails
@app.errorhandler(404)
def page_not_found(e):
    return render_template("error.html",error="Error 404")

@app.errorhandler(500)
def page_not_found(e):
    return render_template("error.html",error="Error 500")


@app.route('/')
def root():
    if "user" in session:
        return render_template('welcome.html')
    return render_template('index.html')


@app.route('/signup')
def signup():
    if "user" in session:
        return render_template('welcome.html')
    return render_template('signup.html')


@app.route('/welcome')
def welcome():
    if "user" in session:
        return render_template('welcome.html')
    return redirect(url_for('root'))    

@app.route('/logout')    
def logout():
    exists = db.session.query(logindetails).filter_by(username=session['user']).first()
    if exists:
        exists.activestatus=False
        db.session.commit()
    session.pop('user',None)
    return redirect(url_for('root'))


@app.route('/', methods=['GET', 'POST'])
def login():
    error = None
    if request.method == 'POST':
        uname = request.form.get("username")
        password1 = request.form.get("password")
        exists=None
        exists = db.session.query(logindetails).filter(logindetails.username==uname,logindetails.password==sha256(password1.encode()).hexdigest()).first()
        if exists:
            exists.activestatus=True
            db.session.commit()
            session["user"]=uname
            return redirect(url_for('welcome'))
        else:
            error = 'Invalid Username or Password'    
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
                return render_template('signup.html', error=error)

            exists = db.session.query(db.session.query(userdetails).filter_by(email=email).exists()).scalar()
            if exists == True:
                error = 'Email id already Exit'
            else:
                new_user = userdetails(username, name, email)
                db.session.add(new_user)
                db.session.commit()
                login=logindetails(username,sha256(password.encode()).hexdigest(),False)
                db.session.add(login)
                db.session.commit()
                return redirect(url_for('root'))

    return render_template('signup.html', error=error)





@app.route('/welcome', methods=['POST'])
def active_users():
    emoji=["far fa-grin-beam-sweat","far fa-smile-wink","far fa-laugh-squint","far fa-kiss-beam","far fa-grin-hearts"]
    color=["text-primary","text-warning","text-dark","text-primary","text-success"]
    result=" "
    j=0
    active= db.session.query(logindetails.username).filter_by(activestatus=True)
    if active:
        for i in active:
            str1 = '''
            <span class="fa-stack p-0" style="font-size:20px" title="'''+i[0]+'''">
            <i class="fa fa-circle fa-stack-2x '''+color[j]+'''" ></i>
            <i class="'''+emoji[j]+''' fa-stack-1x fa-inverse"></i>
            </span>
            '''
            j = j+1
            if j==5:
               j=0
            result += str1
    else:
        result+='None'    
    return result