from app import db


class userdetails(db.Model):
    username = db.Column(db.String(20), primary_key=True)
    name = db.Column(db.String(80), unique=True, nullable=False)
    email = db.Column(db.String(80), unique=True, nullable=False)
    password = db.Column(db.String(80), unique=True, nullable=False)

    def __init__(self, username, name, email, password):
        self.username = username
        self.name = name
        self.email = email
        self.password = password


class logindetails(db.Model):
    username = db.Column(db.String(20), db.ForeignKey('userdetails.username'), primary_key=True)
    password = db.Column(db.String(50), nullable=False)

    def __init___(self, username, password):
        self.username = username
        self.password = password
