
from datetime import datetime

now=datetime.now()
now2 = datetime.timestamp(now)
dt_object = datetime.fromtimestamp(now2)

print("dt_object =", dt_object)