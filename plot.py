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

# initialize the Metadata Object
meta = MetaData(bind=engine)
MetaData.reflect(meta)

#with engine.connect() as con:
statement = text("""select sum(duration) as DURATION_WEEK from learn where 
                            date_added < DATE_TRUNC('week', NOW())
                                AND
                            date_added >= DATE_TRUNC('week', NOW()) - interval '7 day' ;""")

con.execute(statement)

engine.execute(statement)






fig, ax = plt.subplots(figsize=(6, 6))
data = [87, 13]
wedgeprops = {'width':0.3, 'edgecolor':'black', 'lw':3}
patches, _ = ax.pie(data, wedgeprops=wedgeprops, startangle=90, colors=['#5DADE2', 'white'])
patches[1].set_zorder(0)
patches[1].set_edgecolor('white')
plt.title('Worldwide Access to Electricity', fontsize=24, loc='left')
plt.text(0, 0, f"{data[0]}%", ha='center', va='center', fontsize=42)
plt.text(-1.2, -1.3, "Source: ourworldindata.org/energy-access", ha='left', va='top', fontsize=12)
plt.show()

