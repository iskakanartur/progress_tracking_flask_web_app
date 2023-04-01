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


################### MOVED FROM APP. PY ####################
############################ A simple VIZ Setup. change later ###############
@app.route('/plot')
def plot():
    left = [1, 2, 3, 4, 5]
    # heights of bars
    height = [10, 24, 36, 40, 5]
    # labels for bars
    tick_label = ['one', 'two', 'three', 'four', 'five']
    # plotting a bar chart
    plt.bar(left, height, tick_label=tick_label, width=0.8, color=['red', 'green'])

    # naming the y-axis
    plt.ylabel('y - axis')
    # naming the x-axis
    plt.xlabel('x - axis')
    # plot title
    plt.title('My bar chart!')

    plt.savefig('static/images/plot.png')

    ## Temp QUery 
    #filter_after = datetime.today() - timedelta(days = 30)
    #mo_to_sun = Learn.query.filter(Learn.date_added >= filter_after).all()
    mo_to_sun = past_mo_to_sun ()

    return render_template('plot.html', url='/static/images/plot.png', mo_to_sun= mo_to_sun)




