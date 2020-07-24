from app import db
from models import userdetails, logindetails

#create table
db.create_all();

#insert db
new_user=userdetails('test','test','test','test')
db.session.add(new_user)
db.session.commit()

