from os import environ
import settings 



import matplotlib.pyplot as plt
from sqlalchemy import create_engine
from sqlalchemy.sql import text ## To execute plain sql 
import settings


##
# import necessary packages
import sqlalchemy
from sqlalchemy import create_engine, MetaData
from sqlalchemy.engine import result

##

engine = create_engine(f'postgresql://postgres:{settings.pgpw}@localhost/progress')

from sqlalchemy import text

with engine.connect() as connection:
    # result = connection.execute(text("select * from learn"))
    result = connection.execute(text(f"""{settings.total_hours_week_learn}"""))

    #for row in result:
        #print("subject:", row["subject"])
        #print (row)

    for row in result:
        #print("subject:", row["subject"])
        print (row)