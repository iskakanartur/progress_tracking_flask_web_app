from dotenv import dotenv_values

config = dotenv_values(".env") ###### Loads all .env values as a dictionary 


######  Database connection 
pgpw= config['postgres_pw']
sky= config['SECRET_KEY']


####### SQL PLAIN TEXT 
total_hours_week_learn= config['total_hours_week_learn']
mo_to_sun= config['mo_to_sun']

# print (config['mo_to_sun'])
# print (config)
