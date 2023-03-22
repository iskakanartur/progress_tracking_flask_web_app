from dotenv import dotenv_values

config = dotenv_values(".env") ###### Loads all .env values as a dictionary 

pgpw= config['postgres_pw']
sky= config['SECRET_KEY']

