
## WHen First createing the Table Learnries enter flask shell 
## from app import db
## db.create_all()

from flask import Flask, render_template, request, redirect, url_for, flash
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.sql import func
from sqlalchemy import func, text

#from datetime import date, datetime, timedelta
#from datetime import datetime
from datetime import date, datetime, timedelta
from sqlalchemy.types import DateTime
from sqlalchemy.sql import expression
from sqlalchemy import inspect
from sqlalchemy import extract  

from calendar import monthrange

import os
import psycopg2



app = Flask(__name__)

## CHnages this secrets see app1.oy os get 
# app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql://turo:HayastaN77@127.0.0.1/flaskaws'

app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://postgres:TraCak45@localhost/progress'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.secret_key = "somethingunique"


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
    grocs = Learn.query.all()

    max_duration = db.session.query(func.max(Learn.duration)).scalar()
    min_duration = db.session.query(func.min(Learn.duration)).scalar()
    all_time_sum = db.session.query(func.sum(Learn.duration)).scalar()

    
    days_count_final = total_number_of_days ()
    
    all_tme_avg_raw = db.session.query(func.avg(Learn.duration).label('average_duration')).all()
    all_tme_avg = round (all_time_sum/days_count_final, 2)


    return render_template('index.html', grocs=grocs, all_tme_avg=all_tme_avg,
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
        my_data.comment = request.form['comment']
        my_data.duration = request.form['duration']
        my_data.date_added = request.form['date_added']

        db.session.commit()
        flash("Գնումը Գրանցված է")
        return redirect(url_for('index'))


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


