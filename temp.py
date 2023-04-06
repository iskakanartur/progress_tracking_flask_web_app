# If you want to print the full date, simply remove the strftime method from being called.
from datetime import date
from dateutil.relativedelta import relativedelta, MO, SU

today = date.today()
last_monday = today + relativedelta(weekday=MO(-1))
last_sunday = today + relativedelta(weekday=SU(-1))
print (last_monday.strftime("%-m-%d"))
print (last_sunday.strftime("%-m-%d"))
print (last_monday)
print (f"'{last_monday}'")
print (f"'{last_sunday}'")

print ('-'*90)


###  Parts of MO to SU 
    mo_to_sun1 = db.session.query(Learn).filter(Learn.date_added 
                <= func.date_trunc('week', func.now( ) ))
    
    mo_to_sun2 = db.session.query(Learn).filter(Learn.date_added 
                >= func.date_trunc('week', func.now( ) )  -  timedelta(days=7) )

########## OLD WORKING CODE FOR MO_TO 
     # If you want to print the full date, simply remove the strftime method from being called.

from dateutil.relativedelta import relativedelta, MO, SU

today = date.today()
last_monday = today + relativedelta(weekday=MO(-1))
last_sunday = today + relativedelta(weekday=SU(-1))

mo_to_sun = db.session.query(Learn).filter(Learn.date_added.between('2023-03-20', '2023-03-26'))

 #start_range = date.today()  
    #end_range = start_range - timedelta(days=3)

    #start_range = date.today() + timedelta(days=-7)
    #end_range = date.today() + timedelta(days=-3)

    # THIS one works but not what I need
    # # 1 = Sunday, 2 = Monday, ..., 7 = Saturday.
    # mo_to_sun = Learn.query.filter(Learn.date_added.between(start_range, end_range)).all()





################### QUERY INDIVIDUAL SUM OF LEARNING SUBJECTS     #########################
def past_mo_to_sun_subj_sum ():

    from sqlalchemy import and_ ### to combine db queries below
    
    mo_to_sun_sum_subj_sum = db.session.query(Learn).filter (and_( 
        Learn.date_added <= func.date_trunc('week', func.now( ) ), 
        Learn.date_added >= func.date_trunc('week', func.now( ) ) - timedelta(days=7),
        Learn.subject=='SQL')).with_entities(func.sum(Learn.duration)).scalar()
                
    return (mo_to_sun_sum_subj_sum)

################### QUERY INDIVIDUAL SUM OF LEARNING SUBJECTS  #########################
def past_mo_to_sun_subj_sum_fun (subject):

    from sqlalchemy import and_ ### to combine db queries below
    
    mo_to_sun_sum_subj_sum_fun = db.session.query(Learn).filter (and_( 
        Learn.date_added <= func.date_trunc('week', func.now( ) ), 
        Learn.date_added >= func.date_trunc('week', func.now( ) ) - timedelta(days=7),
        Learn.subject== subject)).with_entities(func.sum(Learn.duration)).scalar()
                
    return (mo_to_sun_sum_subj_sum_fun)



 
    ################## LEGENDS FROM MULTI CYCLE PLOT 
    legend_elements =  [Line2D([0], [0], marker='o', color='w', label='Group A',
                            markerfacecolor='#4393E5', markersize=10),
                        Line2D([0], [0], marker='o', color='w', label='Group B', 
                            markerfacecolor='#43BAE5', markersize=10),
                        Line2D([0], [0], marker='o', color='w', label='Group C', 
                               markerfacecolor='#7AE6EA', markersize=10)]
    ################# Legend Elements 2 ver 
    
    subject_titles = [i[0] for i in subjects if i[1]!= None]  ## Get the Subj names from above tuple
    legend_colors = ['#4393E5', '#43BAE5', '#7AE6EA']
    legend_elements =[]

    for legend, color in list(zip(subject_titles, legend_colors)):
        legend_elem =  [Line2D([0], [0], marker='o', color='w', label=f'{legend}',
                            markerfacecolor=f'{color}', markersize=12)]
        legend_elements.append(legend_elem)

        # legend_elements.append((legend, color))