from app import db, Flask
from models import userdetails,logindetails

exists = db.session.query(logindetails).filter_by(username='sharook').first()
if exists:
   exists.activestatus=False
   db.session.commit()

print("Working");
