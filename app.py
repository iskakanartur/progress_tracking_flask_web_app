
## WHen First createing the Table Learnries enter flask shell 
## from app import db
## db.create_all()



 ################## TEMP IMPORTS FOR SIMPLE VIZ PLOT DEL LATER #######
import io
import random
from flask import Response
from matplotlib.backends.backend_agg import FigureCanvasAgg as FigureCanvas
from matplotlib.figure import Figure
import matplotlib.pyplot as plt

################################################

from os import environ
import settings 


from flask import Flask, render_template, request, redirect, url_for, flash
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.sql import func
from sqlalchemy import func, text


from datetime import date, datetime, timedelta
from sqlalchemy.sql import expression
from sqlalchemy import inspect
from sqlalchemy import extract  

from calendar import monthrange

import os
import psycopg2



app = Flask(__name__)


app.config['SQLALCHEMY_DATABASE_URI'] = f'postgresql://postgres:{settings.pgpw}@localhost/progress'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.secret_key = settings.sky


db = SQLAlchemy(app)

#def get_date():
    #return CURRENT_TIMESTAMP;

class Learn(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    subject = db.Column(db.String(150), nullable=False)
    duration = db.Column(db.Integer)
    #date_added = db.Column(db.DateTime, default = gatetime.now)
    date_added = db.Column(db.DateTime(timezone=True), server_default=func.now())
    comment = db.Column(db.String(150), nullable=True)


    def __init__(self, subject, duration, date_added, comment):
        self.subject = subject
        self.duration = duration 
        self.date_added = date_added
        self.comment = comment


########## Helper to filter the month by a month number from the  date_added field
def query_month(month_num):
    qry = Learn.query.filter(extract('month', Learn.date_added)==month_num).all()
    return (qry)


######## Helper to get the total number of days in a given month 
def query_days_month(year,month_num):
    days_in_month = monthrange(year, month_num)
    return (days_in_month)

####### Helper to get the number of total days passed since the start of records
def total_number_of_days ():
    date_query = db.session.query(Learn.date_added).all()
    strt_date = date_query[0][0].replace(tzinfo=None) ## Otherwise Error Tz naive
    end_date = datetime.now()
    total_days_count = strt_date - end_date
    total_days_count_final = total_days_count.days


    return (total_days_count_final)


 


@app.route('/')
def index():
    learn_query_all = Learn.query.all()

    max_duration = db.session.query(func.max(Learn.duration)).scalar()
    min_duration = db.session.query(func.min(Learn.duration)).scalar()
    all_time_sum = db.session.query(func.sum(Learn.duration)).scalar()

    
    days_count_final = total_number_of_days ()
    
    all_tme_avg_raw = db.session.query(func.avg(Learn.duration).label('average_duration')).all()
    all_tme_avg = round (all_time_sum/days_count_final, 2)


    return render_template('index.html', learn_query_all=learn_query_all, all_tme_avg=all_tme_avg,
                            days_count_final=days_count_final,
                            all_time_sum=all_time_sum)
    


##### A ROUTE TO ADD Learnries #############
@app.route('/add/', methods = ['POST'])
def insert_subject():
    if request.method =='POST':
        prod = Learn(
            subject = request.form.get('subject'),
            duration = request.form.get('duration'),
            comment = request.form.get('comment'),
            date_added = request.form.get('date_added')

        )
        db.session.add(prod)
        db.session.commit()
        flash("Ձեր գոնումը հայտնվեց շտեմարանում, Շնորհակալութոյւն")
        return redirect(url_for('index'))


###################### Route to Update ##################
@app.route('/update/', methods = ['POST'])
def update():
    if request.method == "POST":
        my_data = Learn.query.get(request.form.get('id'))

        my_data.subject = request.form['subject']
        my_data.duration = request.form['duration']
        my_data.date_added = request.form['date_added']
        my_data.comment = request.form['comment']

        db.session.commit()
        flash("Գնումը Գրանցված է")
        return redirect(url_for('index'))
    

################################## Get All SUbject Names     ######################
def get_subjects ():
    # subject_names = [subj.subject for subj in Learn.query.all()]
    subject_names = [subj for subj in db.session.query(Learn.subject).distinct()]
    subject_names = [i[0] for i in subject_names]

    return (subject_names)
    

################################## QUERY LAST WEEK MO - SU   ##########################
## See the plain sql version in progress_plain.sql file 
def past_mo_to_sun ():

    from sqlalchemy import and_ ### to combine db queries below
    
    mo_to_sun = db.session.query(Learn).filter (and_(Learn.date_added 
                <= func.date_trunc('week', func.now( ) ), Learn.date_added 
                >= func.date_trunc('week', func.now( ) ) - timedelta(days=7))).order_by(Learn.date_added )
                
    return (mo_to_sun)


###################### QUERY SUM OF past MO to SUN Learning Hours  #########################
def past_mo_to_sun_sum ():

    from sqlalchemy import and_ ### to combine db queries below
    
    mo_to_sun_sum = db.session.query(Learn).filter (and_(Learn.date_added 
                <= func.date_trunc('week', func.now( ) ), Learn.date_added 
                >= func.date_trunc('week', func.now( ) ) - 
                timedelta(days=7))).with_entities(func.sum(Learn.duration)).scalar()
                
    return (mo_to_sun_sum)



################### QUERY TOTAL HOURS LEARNED DISTINCT SUBJECTS - MO-SU  #########################
def subj_total ():

    from sqlalchemy import and_ ### to combine db queries below

    distinct_subjects = get_subjects()
    res = []
    subj_total_sum_mo_su = []
    for subject in distinct_subjects:
        qry_res = mo_to_sun_sum_subj_sum_fun = db.session.query(Learn).filter (and_( 
        Learn.date_added <= func.date_trunc('week', func.now( ) ), 
        Learn.date_added >= func.date_trunc('week', func.now( ) ) - timedelta(days=7),
        Learn.subject== subject)).with_entities(func.sum(Learn.duration)).scalar()

        res.append(qry_res)
        subj_total_sum_mo_su.append((subject, qry_res))

    
    return (subj_total_sum_mo_su)






####################### PLOT THE PROGRES CIRCLE MO - SU        ##########################
@app.route('/progress_plot')
def progress_plot():
    fig, ax = plt.subplots(figsize=(6, 6))

    full_circle = 600 ## 10 hours a week learning 
    week_sum_learning = past_mo_to_sun_sum ()
    percent_complete = round (week_sum_learning/full_circle*100, 1)

    data = [percent_complete, 100- percent_complete]

    wedgeprops = {'width':0.3, 'edgecolor':'black', 'lw':3}
    patches, _ = ax.pie(data, wedgeprops=wedgeprops, startangle=90, colors=['#5DADE2', 'white'])
    patches[1].set_zorder(0)
    patches[1].set_edgecolor('white')
    plt.title('Percent Complete : 10 hours a week ', fontsize=20, loc='left')
    plt.text(0, 0, f"{data[0]}%", ha='center', va='center', fontsize=24)
    plt.savefig('static/images/progress_plot.png')

    mo_to_sun = past_mo_to_sun ()
    
    return render_template('progress_plot.html', 
                           url='/static/images/progress_plot.png', mo_to_sun= mo_to_sun)


############################## MULTI CIRCLE PLOT PROGRESS ###########################
from math import pi
import numpy as np
from matplotlib.patches import Patch
from matplotlib.lines import Line2D
@app.route('/multi_progress_plot')
def multi_progress_plot ():

    fig, ax = plt.subplots(figsize=(6, 6))
    ax = plt.subplot(projection='polar')

    ######### Get individual progres circle data

    subjects = subj_total()                         ## Get the ('subj_name', hours_learned) touple
    data =  [i[1] for i in subjects if i[1]!= None] ## Get the hours_total from the tuple
    subject_titles = [i[0] for i in subjects if i[1]!= None]  ## Get the Subj names from above tuple

    # data = [82, 12, 91]
    full_circle = 600                               ## Total Hours To learn 600 Hours for all subjects
    full_circle_each_subj = 600/(len(data))         ## Average Hours for each Subject from 600 hrs
    progress_full_circle_each_subj = [i/full_circle_each_subj*100 for i in data]   ## % cmplet


    startangle = 90
    colors = ['#4393E5', '#43BAE5', '#7AE6EA']

    # xs = [(i * pi *2)/ 100 for i in data]
    xs = [(i * pi *2)/ full_circle_each_subj for i in data]


    ys = [-0.2, 1, 2.2]
    left = (startangle * pi *2)/ 360 #this is to control where the bar starts
    # plot bars and points at the end to make them round
    for i, x in enumerate(xs):
        ax.barh(ys[i], x, left=left, height=1, color=colors[i])
        ax.scatter(x+left, ys[i], s=350, color=colors[i], zorder=2)
        ax.scatter(left, ys[i], s=350, color=colors[i], zorder=2)
    
    plt.ylim(-4, 4)

    
    legend_elements =  [Line2D([0], [0], marker='o', color='w', label='Group A',
                            markerfacecolor='#4393E5', markersize=10),
                        Line2D([0], [0], marker='o', color='w', label='Group B', 
                            markerfacecolor='#43BAE5', markersize=10),
                        Line2D([0], [0], marker='o', color='w', label='Group C', 
                               markerfacecolor='#7AE6EA', markersize=10)]
    
    ax.legend(handles=legend_elements, loc='center', frameon=False)
    # clear ticks, grids, spines
    plt.xticks([])
    plt.yticks([])
    ax.spines.clear()

    plt.savefig('static/images/multi_progress_plot.png')
    # plt.show()

    mo_to_sun = past_mo_to_sun ()

    return render_template('multi_progress_plot.html', 
                            url='/static/images/multi_progress_plot.png', mo_to_sun= mo_to_sun)

    # return (legend_elements)






                        







#################### RouTe To Last 30 Days Purchases ##################
@app.route('/history')
def history_page():
    seven_day_expenses = Learn.query.filter(Learn.date_added > datetime.now() - timedelta(days=7)).all()
    return render_template('history.html', seven_day_expenses=seven_day_expenses)






################### Januray #####################
@app.route('/january')
def january():
    janr = Learn.query.filter(extract('month', Learn.date_added)==1).all()
    dyz =  monthrange(2023, 1)
    return render_template('january.html',  janr=janr, dyz=dyz)

################ Februrary ######################
@app.route('/february')
def february():
    feb = query_month(2)
    feb_dyz = query_days_month(2023, 2)
    
    return render_template('february.html', feb=feb, feb_dyz=feb_dyz)









if __name__ == "__main__":
    app.run(debug=True)



