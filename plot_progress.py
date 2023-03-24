from os import environ
import settings ## settings.py file wth all settings
from collections import namedtuple ## TO create a named tuple in a query result

import matplotlib.pyplot as plt

from sqlalchemy import create_engine
from sqlalchemy.sql import text ## To execute plain sql 
from sqlalchemy.engine import result


engine = create_engine(f'postgresql://postgres:{settings.pgpw}@localhost/progress')



########### Get The Sum Total hours learned Mo-To_Fri ## Result is a tuple inside list ###
#### Take 10 Hours a week as a base to begin 

def get_sum_total_learning():
    with engine.connect() as connection:
        sum_learn = connection.execute(text(f"""{settings.total_hours_week_learn}"""))

    Record_sum_learn = namedtuple('Record', sum_learn.keys())
    records_sum_learn = [Record_sum_learn(*r) for r in sum_learn.fetchall()]
    total_time_learn = records_sum_learn[0].duration_week
    
    return (total_time_learn)



############################### THE PLOT ###############################

def plot_learning_progress():
    fig, ax = plt.subplots(figsize=(6, 6))

    full_circle = 600 ## 10 hours a weel
    week_sum_learning = get_sum_total_learning()
    percent_complete = round (week_sum_learning/full_circle*100, 1)

    data = [percent_complete, 100- percent_complete]

    wedgeprops = {'width':0.3, 'edgecolor':'black', 'lw':3}
    patches, _ = ax.pie(data, wedgeprops=wedgeprops, startangle=90, colors=['#5DADE2', 'white'])
    patches[1].set_zorder(0)
    patches[1].set_edgecolor('white')
    plt.title('Percent Complete of total 10 hours a week ', fontsize=24, loc='left')
    plt.text(0, 0, f"{data[0]}%", ha='center', va='center', fontsize=42)
    plt.savefig('static/images/plot_progress.png')
    # plt.text(-1.2, -1.3, "Source: ourworldindata.org/energy-access", ha='left', va='top', fontsize=12)
    plt.show()



if __name__ == '__main__':
    plot_learning_progress()

