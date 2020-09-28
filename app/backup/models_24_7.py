from app import db
from datetime import datetime
from sqlalchemy.dialects.postgresql import INET


#from http://flask-appbuilder.readthedocs.io/en/latest/multipledbs.html for dealing with 2 data bases db
class Psps_db(db.Model):
	id = db.Column(db.Integer, primary_key=True)

class Menta_db(db.Model):
	__bind_key__ = 'menta_db'
	id = db.Column(db.Integer, primary_key=True)



	  
########################################## Profile's Strength
strength_relationships=db.Table('stength_relationships',
						   db.Column('profile_id', db.Integer,db.ForeignKey('profile.id')),						   
						   db.Column('strength_id',db.Integer,db.ForeignKey('strength.id'))	
						   )
								 
class Strength(db.Model):
	id = db.Column(db.Integer, primary_key=True)
	title = db.Column(db.String(255), nullable=True)
	selected = db.Column(db.Boolean)
	 
	#dumy_for_test = db.Column(db.Boolean)
	 
	def __init__(self, title):
		self.title=title
		self.selected = False
############################################ Profile's Strength  


########################################## Profile's Weaknesse
weaknesse_relationships=db.Table('weaknesse_relationships',
						   db.Column('profile_id', db.Integer,db.ForeignKey('profile.id')),						   
						   db.Column('weaknesse_id',	 db.Integer,db.ForeignKey('weaknesse.id'))	
						   )
class Weaknesse(db.Model):
	id = db.Column(db.Integer, primary_key=True)
	title = db.Column(db.String(255), nullable=True)
	selected = db.Column(db.Boolean)
		 
	def __init__(self, title):		
		self.title=title
		self.selected = Falsef

############################################ Profile's Weaknesse  



######################################## Interest subjects
interest_subject_relationships=db.Table('interest_subject_relationships',
						    db.Column('profile_id', db.Integer,db.ForeignKey('profile.id')),						   
						    db.Column('interest_subject_id', db.Integer, db.ForeignKey('interest_subject.id'))	
						   )
class Interest_subject(db.Model):
	id = db.Column(db.Integer, primary_key=True)
	title = db.Column(db.String(255), nullable=True)
	selected = db.Column(db.Boolean)
		 
	def __init__(self, title):		
		self.title=title
		self.selected = False
########################################## Interest subjects



######################################## Student's profile
profile_relationships=db.Table('profile_relationships',
						   db.Column('student_id', db.Integer, db.ForeignKey('student.id')),						   
						   db.Column('profile_id', db.Integer, db.ForeignKey('profile.id'))	
						   )
######################################## Student's profile


####################################### Student's staff team
staff_team_relationships=db.Table('staff_team_relationships',
						   db.Column('student_id', db.Integer, db.ForeignKey('student.id')),						   
						   db.Column('team_member_id', db.Integer, db.ForeignKey('team_member.id'))	
						   )
####################################### Student's staff team

####################################### Therapist's clients 
clients_relationships=db.Table('clients_relationships',
						   db.Column('team_member_id', db.Integer, db.ForeignKey('team_member.id')),						   
						   db.Column('student_id', db.Integer, db.ForeignKey('student.id'))	
						   )
####################################### Therapist's clients 

########################################## Role 
s_role_relationships=db.Table('s_role_relationships',
							db.Column('student_id', db.Integer,db.ForeignKey('student.id')), 
							db.Column('role_id',    db.Integer,db.ForeignKey('role.id'))                                                          
                           )
						   
t_role_relationships=db.Table('t_role_relationships',
							db.Column('team_member_id', db.Integer,db.ForeignKey('team_member.id')), 
							db.Column('role_id',        db.Integer,db.ForeignKey('role.id'))                                                          
                           )
						   						   
class Role(db.Model):
	id = db.Column(db.Integer, primary_key=True)
	student_id = db.Column(db.Integer, db.ForeignKey('student.id'))
	team_member_id = db.Column(db.Integer, db.ForeignKey('team_member.id'))
	db.PrimaryKeyConstraint('student_id', 'team_member_id'),
	
	title = db.Column(db.String(140), nullable=True)
	selected = db.Column(db.Boolean)
	
	def __init__(self, student_id, team_member_id):
		self.title="No Role"
		self.student_id=student_id
		self.team_member_id=team_member_id
		self.selected=False
############################################ Role  



####################################### User
class User(db.Model):
	id = db.Column(db.Integer, primary_key=True)
	username = db.Column('username', db.String(20), unique=True , index=True)
	password = db.Column('password' , db.String(10))
	email = db.Column('email',db.String(50),unique=True , index=True)
	registered_on = db.Column('registered_on' , db.DateTime) 

	def __init__(self , username ,password , email):
		self.username = username
		self.password = password
		self.email = email
		self.registered_on = datetime.utcnow()
 
	def is_authenticated(self):
		return True
 
	def is_active(self):
		return True
 
	def is_anonymous(self):
		return False
 
	def get_id(self):
		try:
			return unicode(self.id)  # python 2
		except NameError:
			return str(self.id)	  # python 3
			   
	def add(self,user):
		db.session.add(user)
		return session_commit ()

	def update(self):
		return session_commit()

	def delete(self,user):
		db.session.delete(user)
		return session_commit()

	def __repr__(self):
		return '<User %r>' % (self.username)
####################################### User
 


##################################Student													
class Student(db.Model):
	id = db.Column(db.Integer, primary_key=True)
	first_name = db.Column('first_name', db.String(20))
	last_name = db.Column('last_name', db.String(20), index=True)
	birth_date = db.Column(db.DateTime, nullable = False)
	grade  = db.Column('grade', db.String(10))
	
	timestamp = datetime.utcnow()
	registered_on = db.Column('registered_on' , db.DateTime) 

	selected = db.Column(db.Boolean)
	
	profile=db.relationship('Profile', secondary=profile_relationships, cascade='all,delete', backref='student')

	staff_team_members=db.relationship('Team_member', secondary=staff_team_relationships, backref='student' )
	roles=db.relationship('Role', secondary=s_role_relationships, backref='student' )
	
	def __init__(self, id, first_name, last_name ,birth_date, grade):
		self.id = id
		self.first_name = first_name
		self.last_name = last_name	
		self.birth_date = birth_date
		self.grade = grade
		self.registered_on = datetime.utcnow()

	def add(self,student):
		db.session.add(student)
		return session_commit()

	def update(self):
		return session_commit()

	def delete(self,student):
		db.session.delete(student)
		return session_commit()		  
##################################Student



####################################### Team_member ==> should be inherited from User but i didnt find a technical way to do it. 
class Team_member(db.Model):
	id = db.Column(db.Integer, primary_key=True)
	first_name = db.Column('first_name', db.String(20), index=True)
	last_name = db.Column('last_name', db.String(20), index=True)

	email = db.Column('email',db.String(50),unique=True , index=True)
	registered_on = db.Column('registered_on' , db.DateTime) 
	
	profetional = db.Column(db.String(140), nullable=True)
	#clients=db.relationship('Student', secondary=clients_relationships, cascade='all,delete', backref='team_member') 
	
	selected = db.Column(db.Boolean)
	
	clients=db.relationship('Student', secondary=clients_relationships, backref='team_member' )
	roles=db.relationship('Role', secondary=t_role_relationships, backref='team_member' )
	
	def __init__(self , id, first_name, last_name, profetional, email):
		self.id = id
		self.first_name = first_name
		self.last_name = last_name	
		self.password = profetional
		self.email = email
		self.registered_on = datetime.utcnow()
 
	def is_authenticated(self):
		return True
 
	def is_active(self):
		return True
 
	def is_anonymous(self):
		return False
 
	def get_id(self):
		try:
			return unicode(self.id)  # python 2
		except NameError:
			return str(self.id)	  # python 3
			   
	def add(self,team_member):
		db.session.add(user)
		return session_commit ()

	def update(self):
		return session_commit()

	def delete(self,team_member):
		db.session.delete(team_member)
		return session_commit()

	def __repr__(self):
		return '<User %r>' % (self.first_name)
####################################### Team_member
 



	 
############################################ Profile 	 
class Profile(db.Model):
	id = db.Column(db.Integer, primary_key = True)
	author_id = db.Column(db.Integer, db.ForeignKey('user.id'))
	title = db.Column(db.String(140), nullable=True)
	body = db.Column(db.String(400))
	timestamp = datetime.utcnow()
	selected = db.Column(db.Boolean)
	strength=db.relationship('Strength', secondary=strength_relationships, backref='profile' )  
	weaknesses=db.relationship('Weaknesse', secondary=weaknesse_relationships, backref='profile' )	  
	interest_subject=db.relationship('Interest_subject', secondary=interest_subject_relationships, backref='profile' )
	 
	def __init__(self ,title, body, author_id):
		self.title = title
		self.body = body
		self.author_id = author_id
		self.timestamp = datetime.utcnow()
		self.selected = False
	 
	def add(self,student):
		db.session.add(student)
		return session_commit()

	def update(self):
		return session_commit()

	def delete(self,student):
		db.session.delete(student)
		return session_commit()		  
############################################ Profile 


# from https://github.com/Leo-G/Freddy/blob/master/app/models.py		  
#Universal functions

def  session_commit ():
	try:
		db.session.commit()
	except SQLAlchemyError as e:
		db.session.rollback()
		reason=str(e)
		return reason
