from flask import Flask, render_template,request,redirect,url_for

app=Flask(__name__)

@app.route('/')
def root():
        return render_template('index.html')

@app.route('/',methods=['GET','POST'])
def login():
        error=None
        if request.method == 'POST':
           if request.form['username']!='admin@gmail.com' or request.form['password']!='password':
                error='Invalid Username or Password'
           else:
                error='Success'
                return redirect(url_for('root'))
        return render_template('index.html',error=error)

@app.route('/signup')
def signup():
        return render_template('signup.html');        
