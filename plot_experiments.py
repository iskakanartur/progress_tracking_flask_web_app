# print ('*'*100)

############# QUERY  Mo - to Su Query 
with engine.connect() as connection:
    result = connection.execute(text(f"""{settings.mo_to_sun}"""))


####### Get Results 
from collections import namedtuple

Record = namedtuple('Record', result.keys())
records = [Record(*r) for r in result.fetchall()]
## print optionally 
#for r in records:
    #print(r)

#print ('*'*100)
#print (type(records))
#print (records[0])


