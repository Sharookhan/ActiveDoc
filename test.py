from app import Flask, db
from models import userdetails,logindetails

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
print(result)   