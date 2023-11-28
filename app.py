from flask import Flask, render_template, request, redirect, url_for, session, jsonify
from flask_sqlalchemy import SQLAlchemy
from hashlib import sha256
import random
from datetime import datetime

app = Flask(__name__)
app.secret_key = 'Thisisthesecretkey'
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgres://...your_database_uri_here...'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)
db.init_app(app)

from models import userdetails,logindetails
@app.errorhandler(404)
def page_not_found(e):
    return render_template("error.html",error_img="error_404",error_color="btn-outline-primary")

@app.errorhandler(500)
def page_not_found(e):
    return render_template("error.html",error_img="error_500",error_color="btn-outline-danger")


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
    else:        
        return render_template("error.html",error_img="error_401",error_color="btn-outline-success") 

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
            session['time']=exists.timestamp
            exists.activestatus=True      
            now=datetime.now()
            now2 = datetime.timestamp(now)
            dnow = datetime.fromtimestamp(now2)
            exists.timestamp=dnow
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
                now=datetime.now()
                now2 = datetime.timestamp(now)
                dnow = datetime.fromtimestamp(now2)
                login=logindetails(username,sha256(password.encode()).hexdigest(),dnow,False)
                db.session.add(login)
                db.session.commit()
                session['reg']=True
                
    if error:
        return render_template('signup.html', error=error)
    else:
        return render_template('signup.html', success=True)





@app.route('/welcome', methods=['POST'])
def active_users():
    emoji=["far fa-grin-beam-sweat","far fa-smile-wink","far fa-laugh-squint","far fa-kiss-beam","far fa-grin-hearts"]
    color=["text-primary","text-warning","text-dark","text-primary","text-success"]
    result=" "
    j=0
    active= db.session.query(logindetails.username).filter_by(activestatus=True)
    if active:
        for i in active:
            uactive=db.session.query(userdetails).filter(userdetails.username==i[0]).first()
            str1 = '''
            <span class="fa-stack p-0" style="font-size:20px" title="'''+str(uactive.name)+'''">
            <i class="fa fa-circle fa-stack-2x '''+color[j]+'''" ></i>
            <i class="'''+emoji[j]+''' fa-stack-1x fa-inverse"></i>
            </span>
            '''
            result+=str1
            j = j+1
            if j==5:
                j=0
    else:
        result+='None'    
    return result
