from app import db
from datetime import datetime
from sqlalchemy.dialects.postgresql import INET


#FROM https://stackoverflow.com/questions/26470637/many-to-many-relationship-with-extra-fields-using-wtforms-sqlalchemy-and-flask
from sqlalchemy import event
#from common import UTCDateTime

#FROM https://botproxy.net/docs/how-to/how-to-handle-ordered-many-to-many-relationship-association-proxy-in-flask-admin-form/
from sqlalchemy.ext.associationproxy import association_proxy


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



########################################## Role 			   
class Role(db.Model):
	
	id =    db.Column(db.Integer, primary_key=True)
	student_id = db.Column(db.Integer, db.ForeignKey('student.id'))
	teacher_id = db.Column(db.Integer, db.ForeignKey('teacher.id'))
	title = db.Column(db.String(140), nullable=True)
	selected = db.Column(db.Boolean)
	
	#FROM http://docs.sqlalchemy.org/en/rel_1_0/orm/basic_relationships.html#many-to-many
	#FROM https://botproxy.net/docs/how-to/how-to-handle-ordered-many-to-many-relationship-association-proxy-in-flask-admin-form/
	#teacher = db.relationship('Teacher', backref = 'roles')
	#student = db.relationship('Student', backref = 'roles')

	#FROM http://docs.sqlalchemy.org/en/rel_1_0/orm/basic_relationships.html#many-to-many

	def __init__(self, student_id, teacher_id, title):
		self.title=title
		self.student_id=student_id
		self.teacher_id=teacher_id
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
	
	#FROM http://docs.sqlalchemy.org/en/rel_1_0/orm/basic_relationships.html#many-to-many assosiation with extra data
	#teachers=db.relationship('Teacher', secondary="role", cascade='all,delete', backref='student')

	#FROM https://botproxy.net/docs/how-to/how-to-handle-ordered-many-to-many-relationship-association-proxy-in-flask-admin-form/
	from sqlalchemy.ext.associationproxy import association_proxy
	#teachers = association_proxy('roles', 'teacher')
	
	#https://stackoverflow.com/questions/41270319/how-do-i-query-an-association-table-in-sqlalchemy
	#teachers = db.relationship('Teacher', secondary='roles', backref='student', lazy='dynamic')
	
	#FROM Mega tutorial followers
	'''
	teachers = db.relationship(
        'Teacher', secondary=roles,
        primaryjoin=(roles.c.student_id == id),
        secondaryjoin=(roles.c.student_id == id),
        backref='student', lazy='dynamic')
	'''

		
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



####################################### Teacher ==> should be inherited from User but i didnt find a technical way to do it. 
class Teacher(db.Model):
	id = db.Column(db.Integer, primary_key=True)
	first_name = db.Column('first_name', db.String(20), index=True)
	last_name = db.Column('last_name', db.String(20), index=True)

	email = db.Column('email',db.String(50),unique=True , index=True)
	registered_on = db.Column('registered_on' , db.DateTime) 
	
	profetional = db.Column(db.String(140), nullable=True)
	
	selected = db.Column(db.Boolean)
		
	#FROM https://botproxy.net/docs/how-to/how-to-handle-ordered-many-to-many-relationship-association-proxy-in-flask-admin-form/
	#students = association_proxy('roles', 'student')
	
	#https://stackoverflow.com/questions/41270319/how-do-i-query-an-association-table-in-sqlalchemy
	#students = db.relationship('Student', secondary=role, backref='teacher', lazy='dynamic')
	
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
			   
	def add(self,teacher):
		db.session.add(user)
		return session_commit ()

	def update(self):
		return session_commit()

	def delete(self,teacher):
		db.session.delete(teacher)
		return session_commit()

	def __repr__(self):
		return '<User %r>' % (self.first_name)
####################################### Teacher

#FROM https://stackoverflow.com/questions/26470637/many-to-many-relationship-with-extra-fields-using-wtforms-sqlalchemy-and-flask
	'''
    def to_dict(self):
        return {
            'teacher_id': self.id,
            'teacher_first_name': self.first_name,
			'teacher_last_name': self.teacher_last_name,
        }
	'''
#FROM https://stackoverflow.com/questions/26470637/many-to-many-relationship-with-extra-fields-using-wtforms-sqlalchemy-and-flask


#FROM https://www.pythoncentral.io/sqlalchemy-association-tables/  assosiation table with extra data DepartmentEmployeeLink

#FROM https://www.pythoncentral.io/sqlalchemy-association-tables/  assosiation table with extra data DepartmentEmployeeLink


	 
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
