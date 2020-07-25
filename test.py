from app import db, Flask
from models import userdetails, logindetails

try:
      
   color = ["text-primary", "text-warning","text-dark", "text-primary", "text-success"]
   result = " "
   j = 0
   active = db.session.query(logindetails.username).filter_by(activestatus=True)
   if active:
      for i in active:
         str1 = '''
         <span class="fa-stack p-0" style="font-size:20px" title="'''+i[0]+'''">
         <i class="fa fa-circle fa-stack-2x '''+color[j]+'''" ></i>
         <i class="'''+get_emoji()+''' fa-stack-1x fa-inverse"></i>
         </span>
         '''
         j = j+1
         if j==5:
            j= 0
         result += str1
   else:
      result += 'No user'
except expression as identifier:
   print(Exception.values)
print(result)
