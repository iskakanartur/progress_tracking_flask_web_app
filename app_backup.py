################################# #EXPENSES LATEST MODIFICATIONS ############################


# https://www.youtube.com/watch?v=DRWRq3ad0pI
# https://github.com/parwiz123/flaskec2/blob/main/app.py


# Stopped at 28 minutes
### IMPORTANT NOTES !!!!!!!!!!!!!!!!!!!!
# 1 pip install mysqlclient is here for mysql for postgres see other
# 2 index.html - You can truncate postgres timezone display in brwoser with 
# {{ user.last_login_date.strftime('%Y-%m-%d %H:%M:%S') }} striftime() method - No need to change SQL
# 3 Because of Dark Theme in Base Modal Content is white and can't see labels
#  {{(all_tme_avg[0][0])|round }} round in a jinja loop 

## WHen First createing the Table groceries enter flask shell 
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

app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://postgres:TraCak45@localhost/expenses'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.secret_key = "somethingunique"


db = SQLAlchemy(app)

#def get_date():
    #return CURRENT_TIMESTAMP;

class Groce(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    product = db.Column(db.String(150), nullable=False)
    comment = db.Column(db.String(150), nullable=False)
    price = db.Column(db.Float)
    #date_added = db.Column(db.DateTime, default = gatetime.now)
    date_added = db.Column(db.DateTime(timezone=True), server_default=func.now())


    def __init__(self, product, comment, price, date_added):
        self.product = product
        self.comment = comment
        self.price = price
        self.date_added = date_added

######################################## HELPER FUNCTIONS ##################################

########## Helper to filter the month by a month number from the  date_added field
def query_month(month_num):
    qry = Groce.query.filter(extract('month', Groce.date_added)==month_num).all()
    return (qry)


######## Helper to get the total number of days in a given month 
def query_days_month(year,month_num):
    days_in_month = monthrange(year, month_num)
    return (days_in_month)

####### Helper to get the number of total days passed since the start of records
def total_number_of_days ():
    date_query = db.session.query(Groce.date_added).all()
    strt_date = date_query[0][0].replace(tzinfo=None) ## Otherwise Error Tz naive
    end_date = datetime.now()
    total_days_count = strt_date - end_date
    total_days_count_final = total_days_count.days


    return (total_days_count_final)




@app.route('/')
def index():
    grocs = Groce.query.all()

    max_price = db.session.query(func.max(Groce.price)).scalar()
    min_price = db.session.query(func.min(Groce.price)).scalar()
    all_time_sum = db.session.query(func.sum(Groce.price)).scalar()

    
    days_count_final = total_number_of_days ()
    
    all_tme_avg_raw = db.session.query(func.avg(Groce.price).label('average_price')).all()
    all_tme_avg = round (all_time_sum/days_count_final, 2)


    return render_template('index.html', grocs=grocs, all_tme_avg=all_tme_avg,
                            days_count_final=days_count_final,
                            all_time_sum=all_time_sum)
    


##### A ROUTE TO ADD Groceries #############
@app.route('/add/', methods = ['POST'])
def insert_product():
    if request.method =='POST':
        prod = Groce(
            product = request.form.get('product'),
            comment = request.form.get('comment'),
            price = request.form.get('price'),
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
        my_data = Groce.query.get(request.form.get('id'))

        my_data.product = request.form['product']
        my_data.comment = request.form['comment']
        my_data.price = request.form['price']
        my_data.date_added = request.form['date_added']

        db.session.commit()
        flash("Գնումը Գրանցված է")
        return redirect(url_for('index'))


#################### RouTe To Last 30 Days Purchases ##################
@app.route('/history')
def history_page():
    seven_day_expenses = Groce.query.filter(Groce.date_added > datetime.now() - timedelta(days=7)).all()
    return render_template('history.html', seven_day_expenses=seven_day_expenses)






################### Januray #####################
@app.route('/january')
def january():
    janr = Groce.query.filter(extract('month', Groce.date_added)==1).all()
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

