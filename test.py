from app import db, Flask
from models import userdetails,logindetails
import random

result = " "
active = db.session.query(userdetails.name).all()


def get_emoji():
    e1 = "far fa-grin-beam-sweat"
    e2 = "far fa-smile-wink"
    e3 = "far fa-laugh-squint"
    e4 = "far fa-kiss-beam"
    e5 = "far fa-grin-hearts"
    n = random.randint(1, 5)
    if n == 1:
        return e1
    elif n == 2:
        return e2
    elif n == 3:
        return e3
    elif n == 4:
        return e4
    else:
        return e5


def get_color():
    e1 = "text-danger"
    e2 = "text-yellow"
    e3 = "text-dark"
    e4 = "text-primary"
    e5 = "text-success"
    n = random.randint(1, 5)
    if n == 1:
        return e1
    elif n == 2:
        return e2
    elif n == 3:
        return e3
    elif n == 4:
        return e4
    else:
        return e5


color = ["text-danger", "text-yellow",
    "text-dark", "text-primary", "text-success"]
j = 0
result = ""
active= db.session.query(userdetails.name).filter_by(username=db.session.query(logindetails.username).filter_by(activestatus=True))
for i in active:
        str1 = '''
        <span class="fa-stack p-0" style="font-size:20px" title="'''+i[0]+'''">
        <i class="fa fa-circle fa-stack-2x '''+color[j]+'''" ></i>
        <i class="'''+get_emoji()+''' fa-stack-1x fa-inverse"></i>
        </span>
        '''
        j = j+1
        if j==5:
            j=0
        result += str1
print(result)
