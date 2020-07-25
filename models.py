from app import db


class userdetails(db.Model):
    username = db.Column(db.String(20), primary_key=True)
    name = db.Column(db.String(80),nullable=False)
    email = db.Column(db.String(80), unique=True, nullable=False)

    def __init__(self, uname, name, email):
        self.username = uname
        self.name = name
        self.email = email


class logindetails(db.Model):
    username = db.Column(db.String(20), db.ForeignKey('userdetails.username'), primary_key=True)
    password = db.Column(db.String(80), nullable=False)
    timestamp= db.Column(db.DateTime,nullable=False)
    activestatus = db.Column(db.Boolean, nullable=False)

    def __init__(self, username, password,timestamp, activestatus):
        self.username = username
        self.password = password
        self.timestamp=timestamp
        self.activestatus = activestatus
