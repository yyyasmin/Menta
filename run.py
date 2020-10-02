#!flask/bin/python

from app import create_app, db
from app.models import User, Student, Teacher, Profile, Strength, Weakness, Role, Goal, Accupation

app = create_app()
           
if __name__ == "__main__":
	print("Running main with debug mode")
	#FROM https://stackoverflow.com/questions/31264826/start-a-flask-application-in-separate-thread
	#FROM https://stackoverflow.com/questions/38822829/sqlalchemy-raises-queuepool-limit-of-size-10-overflow-10-reached-connection-tim/47151701#47151701
	app.run(debug=True)
            
#if running on heroku these 3 lines shouldnt be running- delete them