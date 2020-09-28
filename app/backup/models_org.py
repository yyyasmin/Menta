#FROM https://github.com/miguelgrinberg/microblog/blob/v0.15/app/models.py3#from hashlib import md5
from flask import current_app
from app import db, login
#FROM https://github.com/miguelgrinberg/microblog/blob/v0.15/app/models.py

from datetime import datetime
from sqlalchemy.dialects.postgresql import INET
	
#FROM https://stackoverflow.com/questions/26470637/many-to-many-relationship-with-extra-fields-using-wtforms-sqlalchemy-and-flask
from sqlalchemy import event
#from common import UTCDateTime

#FROM https://botproxy.net/docs/how-to/how-to-handle-ordered-many-to-many-relationship-association-proxy-in-flask-admin-form/
from sqlalchemy.ext.associationproxy import association_proxy


     		
############################################ Dst Form for cascade dropdown display     
### For cascade dropdown FROM https://github.com/PrettyPrinted/dynamic_select_flask_wtf_javascript
### FROM https://www.tutorialspoint.com/flask/flask_wtf.htm
from flask_wtf import Form
from wtforms import TextField, TextAreaField, SubmitField, DateField , FieldList, FormField, IntegerField
from wtforms import SelectField, validators, ValidationError
### For cascade dropdown FROM https://github.com/PrettyPrinted/dynamic_select_flask_wtf_javascript
from flask import jsonify
from flask_wtf import FlaskForm 
from wtforms.fields.html5 import DateField


#FROM https://hackersandslackers.com/forms-in-flask-wtforms/
from wtforms import (StringField,
                     TextAreaField,
                     SubmitField,
                     PasswordField,
                     DateField,
                     SelectField)
### For cascade dropdown FROM https://github.com/PrettyPrinted/dynamic_select_flask_wtf_javascript

### FROM https://stackoverflow.com/questions/46036966/flask-wtform-validation-failing-for-selectfield-why
### FROM https://stackoverflow.com/questions/46036966/flask-wtform-validation-failing-for-selectfield-why


#FROM https://stackoverflow.com/questions/7979548/how-to-render-my-textarea-with-wtforms
from wtforms.fields import StringField
from wtforms.widgets import TextArea


#from http://flask-appbuilder.readthedocs.io/en/latest/multipledbs.html for dealing with 2 data bases db
class Psps_db(db.Model):
	id = db.Column(db.Integer, primary_key=True)

class Menta_db(db.Model):
	__bind_key__ = 'menta_db'
	id = db.Column(db.Integer, primary_key=True)


	  
########################################## Profile's Strength
profile_strength_relationships=db.Table('profile_strength_relationships',
						   db.Column('profile_id', db.Integer,db.ForeignKey('profile.id')),						   
						   db.Column('strength_id',db.Integer,db.ForeignKey('strength.id'))	
						   )
								 
class Strength(db.Model):
	id = db.Column(db.Integer, primary_key=True)
	author_id = db.Column(db.Integer, db.ForeignKey('user.id'))
	timestamp = datetime.utcnow()
	
	title = db.Column(db.String(255),nullable=True)
	body = db.Column(db.String(400), nullable=True)
	
	selected = db.Column(db.Boolean)

	def __init__(self, title, body, author_id):		
		self.title= title
		self.body = body
		self.author_id = author_id
		self.selected = False
############################################ Profile's Strength  


########################################## Profile's weakness
profile_weakness_relationships=db.Table('profile_weakness_relationships',
						   db.Column('profile_id', db.Integer,db.ForeignKey('profile.id')),						   
						   db.Column('weakness_id',	 db.Integer,db.ForeignKey('weakness.id'))	
						   )
class Weakness(db.Model):
	id = db.Column(db.Integer, primary_key=True)
	author_id = db.Column(db.Integer, db.ForeignKey('user.id'))
	timestamp = datetime.utcnow()
	
	title = db.Column(db.String(255),nullable=True)
	body = db.Column(db.String(400), nullable=True)
	
	selected = db.Column(db.Boolean)

	def __init__(self, title, body, author_id):		
		self.title= title
		self.body = body
		self.author_id = author_id
		self.selected = False

############################################ Profile's weakness  



######################################## Profile's Interest subjects
profile_subject_relationships=db.Table('profile_subject_relationships',
						    db.Column('profile_id', db.Integer,db.ForeignKey('profile.id')),						   
						    db.Column('subject_id', db.Integer, db.ForeignKey('subject.id'))	
						   )
class Subject(db.Model):
	id = db.Column(db.Integer, primary_key=True)
	author_id = db.Column(db.Integer, db.ForeignKey('user.id'))
	timestamp = datetime.utcnow()
	
	title = db.Column(db.String(255),nullable=True)
	body = db.Column(db.String(400), nullable=True)
	
	selected = db.Column(db.Boolean)

	def __init__(self, title, body, author_id):		
		self.title= title
		self.body = body
		self.author_id = author_id
		self.selected = False

########################################## Profile's Interest subjects



######################################## Student's profile
std_profile_relationships=db.Table('std_profile_relationships',
						   db.Column('student_id', db.Integer, db.ForeignKey('student.id')),						   
						   db.Column('profile_id', db.Integer, db.ForeignKey('profile.id'))	
						   )
######################################## Student's profile


######################################## Student's destinations
std_dst_relationships=db.Table('std_dst_relationships',
					   db.Column('student_id',     db.Integer,db.ForeignKey('student.id')),                           
					   db.Column('destination_id', db.Integer,db.ForeignKey('destination.id'))    
					   )
######################################## Student's destinations


							 
#####################Student_dest##################### Dst Tag			   

class Dst_Tag(db.Model):

	#FROM https://stackoverflow.com/questions/40521770/why-am-i-getting-sqlalchemy-error-table-args-value-must-be-a-tuple-dict-o
	__table_args__ = (db.UniqueConstraint('destination_id', 'tag_id', name='destination_tag_pk'), )
	#FROM http://docs.sqlalchemy.org/en/rel_0_9/orm/basic_relationships.html#association-object 
	#id = db.Column(db.Integer, primary_key=True)
		
	destination_id = db.Column(db.Integer, db.ForeignKey('destination.id'), primary_key=True)
	tag_id =    db.Column(db.Integer,      db.ForeignKey('tag.id'),         primary_key=True)
	
	title = db.Column(db.String(140))
	selected = db.Column(db.Boolean)
	
	#FROM http://docs.sqlalchemy.org/en/latest/orm/basic_relationships.html#association-object
	tag = db.relationship("Tag", back_populates="destinations")
	destination = db.relationship("Destination", back_populates="tags")

	def __init__(self, destination_id, tag_id):
		self.destination_id=destination_id
		self.tag_id=tag_id
		self.selected=False
############################################ Dst Tag



########################################## Tag
school_tag_relationships=db.Table('school_tag_relationships',
                           db.Column('school_id', db.Integer,db.ForeignKey('school.id')),                           
                           db.Column('tag_id',    db.Integer,db.ForeignKey('tag.id'))    
                           )
                          
class Tag(db.Model):
    id =    db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(255), nullable=True)
    body = db.Column(db.String(400), nullable=True)	

    selected = db.Column(db.Boolean)
    hide = db.Column(db.Boolean)

    students = db.relationship("Std_tag",     back_populates="tag", cascade="all, delete")
    destinations = db.relationship("Dst_Tag", back_populates="tag", cascade="all, delete")

    def __init__(self, title, body):
        self.title=title
        self.body=body

        self.selected = False
        self.hide = False
        
    def __repr__(self):
        return '<Tag %r>' % self.title

############################################ Tag  



####################################### Age_range 
class Age_range(db.Model):
    id = db.Column(db.Integer, primary_key=True)

    title = db.Column(db.String(140))
    body = db.Column(db.String(400))
    
    from_age = db.Column(db.Integer)
    to_age = db.Column(db.Integer)
    
    selected = db.Column(db.Boolean)
    hide = db.Column(db.Boolean)
    
    destinations = db.relationship('Destination', backref='age_range')

    def __init__(self, title, from_age, to_age, author_id):
        self.title = title
        self.author_id = author_id
        self.from_age = from_age
        self.to_age = to_age
        self.selected = False
        self.hide = False
####################################### Age_range



####################################### Security 
class Scrt(db.Model):     #security of destination 
    id = db.Column(db.Integer, primary_key=True)

    title = db.Column(db.String(140))
    body = db.Column(db.String(400))
    public = db.Column(db.Boolean)
    
    selected = db.Column(db.Boolean)
    hide = db.Column(db.Boolean)
    
    destinations = db.relationship('Destination', backref='scrt')

    def __init__(self, title, author_id):
        self.title = title
        self.author_id = author_id
        self.selected = False
        self.hide = False
####################################### Security

########################################## student_school_relatioship 
student_school_relationships=db.Table('student_school_relationships',
                           db.Column('school_id', db.Integer,db.ForeignKey('school.id')),                           
                           db.Column('student',   db.Integer,db.ForeignKey('student.id'))    
                           )
########################################## student_school_relatioship


########################################## teacher_school_relatioship 
teacher_school_relationships=db.Table('teacher_school_relationships',
                           db.Column('school_id', db.Integer,db.ForeignKey('school.id')),                           
                           db.Column('teacher',   db.Integer,db.ForeignKey('teacher.id'))    
                           )
########################################## student_school_relatioship


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


########################################## Todo 
class Todo(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    
    dst_id =  db.Column(db.Integer, db.ForeignKey('destination.id'))    
    goal_id =  db.Column(db.Integer, db.ForeignKey('goal.id')) 
    title = db.Column(db.String(400))
    body =  db.Column(db.String(500))
    
    who_id =  db.Column(db.Integer, db.ForeignKey('accupation.id'))
    who_title =  db.Column(db.String(140))         
    
    status_id =     db.Column(db.Integer, db.ForeignKey('status.id'))         
    status_title =  db.Column(db.String(300))
    status_color =  db.Column(db.String(10))
  

    selected = db.Column(db.Boolean)
    hide =     db.Column(db.Boolean)

    students = db.relationship("Std_todo", back_populates="todo", cascade="all, delete")

    def __init__(self, title, body, author_id):
        self.title = title
        self.body = body
        self.author_id = author_id
        self.selected = False
        self.hide = False

############################################ Todo


############################################ Todo_form
#FROM https://stackoverflow.com/questions/7979548/how-to-render-my-textarea-with-wtforms
########################################## Todo     
class Todo_form(FlaskForm):
    id = db.Column(db.Integer, primary_key=True)
    
    goal_id =  db.Column(db.Integer, db.ForeignKey('goal.id'))
    dst_id =  db.Column(db.Integer, db.ForeignKey('destination.id'))

    title = TextField("כותרת משימה",[validators.Required("יש להכניס מטרה")])                                   
    body =  TextField("תאור משימה", render_kw={"rows": 70, "cols": 11})
    
    who = SelectField('תפקיד מבצע המשימה', choices=[], validators=[validators.Required(message=('יש לבחור מבצע למשימה'))])
    status = SelectField('סטאטוס ביצוע', choices=[],   validators=[validators.Required(message=('יש לבחור סטאטוס ביצוע'))])
    due_date =  DateField('due_date')

    selected = db.Column(db.Boolean)
    hide =     db.Column(db.Boolean)
    
    submit = SubmitField("שמור משימה")	
    
############################################ Todo_form


########################################## Role 			   
class Role(db.Model):

	#FROM https://stackoverflow.com/questions/40521770/why-am-i-getting-sqlalchemy-error-table-args-value-must-be-a-tuple-dict-o
	__table_args__ = (db.UniqueConstraint('student_id', 'teacher_id', name='student_teacher_pk'), )

	student_id = db.Column(db.Integer, db.ForeignKey('student.id'), primary_key=True)
	teacher_id = db.Column(db.Integer, db.ForeignKey('teacher.id'), primary_key=True)
	
	title = db.Column(db.String(140), nullable=True)
	selected = db.Column(db.Boolean)
	

	#FROM http://docs.sqlalchemy.org/en/latest/orm/basic_relationships.html#association-object
	teacher = db.relationship("Teacher", back_populates="students")
	student = db.relationship("Student", back_populates="teachers")

	def __init__(self, student_id, teacher_id, title):
		self.title=title
		self.student_id=student_id
		self.teacher_id=teacher_id
		self.selected=False
############################################ Role



########################################## Std_tag 			   
class Std_tag(db.Model):

    #FROM https://stackoverflow.com/questions/40521770/why-am-i-getting-sqlalchemy-error-table-args-value-must-be-a-tuple-dict-o

    __table_args__ = (db.UniqueConstraint('student_id', 'tag_id', name='student_tag_pk'), )

    student_id = db.Column(db.Integer, db.ForeignKey('student.id'),      primary_key=True)
    tag_id = db.Column(db.Integer,     db.ForeignKey('tag.id'),  primary_key=True)   

    tag_title = db.Column(db.String(300))
    tag_body =  db.Column(db.String(500))
    
    status_id = db.Column(db.Integer,  db.ForeignKey('status.id'))
    status_title = db.Column(db.String(200))
    status_color = db.Column(db.String(10))

    due_date = db.Column(db.Date)

    selected = db.Column(db.Boolean)
    hide =     db.Column(db.Boolean)


    #FROM http://docs.sqlalchemy.org/en/latest/orm/basic_relationships.html#association-object
    tag =     db.relationship("Tag",     back_populates="students")
    student = db.relationship("Student", back_populates="tags")

    def __init__(self, student_id, tag_id):
        self.student_id=student_id
        self.tag_id=tag_id
        self.selected=False
        self.hide=False

############################################ Std_tag



########################################## Std_destination 			   
class Std_destination(db.Model):

    #FROM https://stackoverflow.com/questions/40521770/why-am-i-getting-sqlalchemy-error-table-args-value-must-be-a-tuple-dict-o

    __table_args__ = (db.UniqueConstraint('student_id', 'destination_id', name='student_destination_pk'), )

    student_id = db.Column(db.Integer,     db.ForeignKey('student.id'),      primary_key=True)
    destination_id = db.Column(db.Integer, db.ForeignKey('destination.id'),  primary_key=True)   
    
    destination_title = db.Column(db.String(300))
    destination_body =  db.Column(db.String(500))
    
    status_id = db.Column(db.Integer,  db.ForeignKey('status.id'))
    status_title = db.Column(db.String(200))
    status_color = db.Column(db.String(10))

    due_date = db.Column(db.Date)

    selected = db.Column(db.Boolean)
    hide =     db.Column(db.Boolean)


    #FROM http://docs.sqlalchemy.org/en/latest/orm/basic_relationships.html#association-object
    destination = db.relationship("Destination", back_populates="students")
    student =     db.relationship("Student",     back_populates="destinations")

    def __init__(self, student_id, destination_id):
        self.student_id=student_id
        self.destination_id=destination_id
        self.selected=False
        self.hide=False

############################################ Std_destination



########################################## Std_goal 			   
class Std_goal(db.Model):

    #FROM https://stackoverflow.com/questions/40521770/why-am-i-getting-sqlalchemy-error-table-args-value-must-be-a-tuple-dict-o

    __table_args__ = (db.UniqueConstraint('student_id', 'goal_id', name='student_goal_pk'), )

    student_id = db.Column(db.Integer, db.ForeignKey('student.id'),      primary_key=True)
    goal_id = db.Column(db.Integer,    db.ForeignKey('goal.id'),         primary_key=True)   
    dst_id =    db.Column(db.Integer,  db.ForeignKey('destination.id'))

    goal_title = db.Column(db.String(300))
    goal_body =  db.Column(db.String(500))
    
    status_id = db.Column(db.Integer,  db.ForeignKey('status.id'))
    status_title = db.Column(db.String(200))
    status_color = db.Column(db.String(10))

    due_date = db.Column(db.Date)

    selected = db.Column(db.Boolean)
    hide =     db.Column(db.Boolean)


    #FROM http://docs.sqlalchemy.org/en/latest/orm/basic_relationships.html#association-object
    goal =    db.relationship("Goal",    back_populates="students")
    student = db.relationship("Student", back_populates="goals")

    def __init__(self, student_id, goal_id):
        self.student_id=student_id
        self.goal_id=goal_id
        self.selected=False
        self.hide=False

############################################ Std_goal


### FROM https://stackoverflow.com/questions/44242802/python-flask-validate-selectfield
class Std_goal_form(FlaskForm):

    goal_id = IntegerField('מספר היעד')  
    goal_title = TextField("כותרת מטרה",[validators.Required("יש להכניס מטרה")])                                   
    goal_body =  TextField("תאור מטרה", render_kw={"rows": 70, "cols": 11})

    status =   SelectField('סטאטוס', choices=[], validators=[validators.Required(message=('יש לבחור סטאטוס'))], coerce=int)                      
    due_date = db.Column(db.Date)
        
    submit = SubmitField("שמור יעד")
    
    ### FROM https://stackoverflow.com/questions/44242802/python-flask-validate-selectfield
    def validate_ar(form):
        if  not form.status.data == None:
          raise ValidationError('יש לבחור סטאטוס')

############################################ Dst Form for cascade dropdown display     


########################################## Std_todo 			   
class Std_todo(db.Model):

    #FROM https://stackoverflow.com/questions/40521770/why-am-i-getting-sqlalchemy-error-table-args-value-must-be-a-tuple-dict-o

    __table_args__ = (db.UniqueConstraint('student_id', 'todo_id', name='student_todo_pk'), )

    student_id = db.Column(db.Integer, db.ForeignKey('student.id'), primary_key=True)
    todo_id = db.Column(db.Integer,    db.ForeignKey('todo.id'),    primary_key=True)      
    dst_id =  db.Column(db.Integer,  db.ForeignKey('destination.id'))
    goal_id = db.Column(db.Integer,  db.ForeignKey('goal.id')) 

    todo_title = db.Column(db.String(400) , nullable=True)
    todo_body = db.Column(db.String(500) ,  nullable=True)

    who_id =    db.Column(db.Integer, db.ForeignKey('accupation.id'))
    who_title = db.Column(db.String(140))         

    status_id =     db.Column(db.Integer, db.ForeignKey('status.id'))         
    status_title =  db.Column(db.String(200))
    status_color =  db.Column(db.String(10))

    due_date = db.Column(db.Date)

    selected = db.Column(db.Boolean)
    hide =     db.Column(db.Boolean)


    #FROM http://docs.sqlalchemy.org/en/latest/orm/basic_relationships.html#association-object
    todo =    db.relationship("Todo",    back_populates="students")
    student = db.relationship("Student", back_populates="todos")

    def __init__(self, student_id, todo_id):
        self.student_id=student_id
        self.todo_id=todo_id
        self.selected=False
        self.hide=False

############################################ Std_todo


########################################## Std_resource 			   
class Std_resource(db.Model):

    #FROM https://stackoverflow.com/questions/40521770/why-am-i-getting-sqlalchemy-error-table-args-value-must-be-a-tuple-dict-o

    __table_args__ = (db.UniqueConstraint('student_id', 'resource_id', name='student_resource_pk'), )

    student_id = db.Column(db.Integer,  db.ForeignKey('student.id'),  primary_key=True)
    resource_id = db.Column(db.Integer, db.ForeignKey('resource.id'), primary_key=True)

    dst_id =  db.Column(db.Integer, db.ForeignKey('destination.id'))
    goal_id = db.Column(db.Integer, db.ForeignKey('goal.id')) 

    who_id =    db.Column(db.Integer, db.ForeignKey('accupation.id'))
    who_title = db.Column(db.String(140))         

    status_id =     db.Column(db.Integer, db.ForeignKey('status.id'))         
    status_title =  db.Column(db.String(200))
    status_color =  db.Column(db.String(10))

    due_date = db.Column(db.Date)


    title = db.Column(db.String(200), nullable=True)
    body =  db.Column(db.String(500), nullable=True)

    selected = db.Column(db.Boolean)
    hide =     db.Column(db.Boolean)

    #FROM http://docs.sqlalchemy.org/en/latest/orm/basic_relationships.html#association-object
    resource = db.relationship("Resource", back_populates="students")
    student =  db.relationship("Student",  back_populates="resources")

    def __init__(self, student_id, resource_id):
        self.student_id=student_id
        self.resource_id=resource_id
        self.selected=False
        self.hide=False

############################################ Std_resource


########################################## Std_document 			   
class Std_document(db.Model):

    #FROM https://stackoverflow.com/questions/40521770/why-am-i-getting-sqlalchemy-error-table-args-value-must-be-a-tuple-dict-o

    __table_args__ = (db.UniqueConstraint('student_id', 'document_id', name='student_document_pk'), )

    student_id = db.Column(db.Integer,  db.ForeignKey('student.id'),  primary_key=True)
    document_id = db.Column(db.Integer, db.ForeignKey('document.id'), primary_key=True)
 
    timestamp = datetime.utcnow()

    title = db.Column(db.String(200), nullable=True)
    body =  db.Column(db.String(500), nullable=True)

    selected = db.Column(db.Boolean)
    hide =     db.Column(db.Boolean)

    #FROM http://docs.sqlalchemy.org/en/latest/orm/basic_relationships.html#association-object
    document = db.relationship("Document", back_populates="students")
    student =  db.relationship("Student",  back_populates="documents")

    def __init__(self, student_id, document_id):
        self.student_id=student_id
        self.document_id=document_id
        self.selected=False
        self.hide=False
        self.timestamp = datetime.utcnow()

############################################ Std_document



####################################### Accupation 
class Status(db.Model):
    id = db.Column(db.Integer, primary_key=True)

    title = db.Column(db.String(140))
    body = db.Column(db.String(400))
        
    selected = db.Column(db.Boolean)
    hide = db.Column(db.Boolean)

    color = db.Column(db.String(10))

    def __init__(self, title, body):
        self.title = title
        self.body = body
        self.color = '#0033cc'
        self.selected = False
        self.hide = False
####################################### Accupation

  
############################################ School						  
class School(db.Model):
    id = db.Column(db.Integer, primary_key = True)
    name = db.Column('first_name', db.String(20))
    timestamp = datetime.utcnow()
    selected = db.Column(db.Boolean)
    tags=db.relationship('Tag',         secondary=school_tag_relationships, backref='school' )  
    students=db.relationship('Student', secondary=student_school_relationships, backref='school' ) 	
    teachers=db.relationship('Teacher', secondary=teacher_school_relationships, backref='school' ) 	
	
    def __init__(self ,id, name):
        self.id = id
        self.name = name
        self.timestamp = datetime.utcnow()
        self.selected = False
	
    def add(self,school):
        db.session.add(school)
        return session_commit()

    def update(self):
        return session_commit()

    def delete(self,school):
        db.session.delete(school)
        return session_commit()
############################################ School						  


		
##################################Student													
class Student(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    first_name = db.Column('first_name', db.String(20))
    last_name = db.Column('last_name', db.String(20), index=True)
    birth_date = db.Column(db.Date, nullable = False)
    grade  = db.Column('grade', db.String(10))
    background = db.Column('background', db.String)
    
    timestamp = datetime.utcnow()
    registered_on = db.Column('registered_on' , db.Date) 

    selected = db.Column(db.Boolean)
    hide = db.Column(db.Boolean)

    profile_id = db.Column(db.Integer, db.ForeignKey('profile.id'), nullable=True)

    #FROM http://docs.sqlalchemy.org/en/latest/orm/basic_relationships.html#association-object

    teachers =  db.relationship("Role",               back_populates="student", cascade="all, delete")
    tags = db.relationship("Std_tag",                 back_populates="student", cascade="all, delete")
    destinations = db.relationship("Std_destination", back_populates="student", cascade="all, delete")
    goals =     db.relationship("Std_goal",           back_populates="student", cascade="all, delete")
    todos =     db.relationship("Std_todo",           back_populates="student", cascade="all, delete")
    resources = db.relationship("Std_resource",       back_populates="student", cascade="all, delete")
    documents = db.relationship("Std_document",       back_populates="student", cascade="all, delete")
        
    def __init__(self, id, first_name, last_name ,birth_date, grade):
        self.id = id
        self.first_name = first_name
        self.last_name = last_name	
        self.birth_date = birth_date
        self.grade = grade
        self.registered_on = datetime.utcnow()
        self.selected = False
        self.hide = False

        

    def add(self,student):
        db.session.add(student)
        return session_commit()

    def update(self):
        return session_commit()

    def delete(self,student):
        db.session.delete(student)
        return session_commit()		

    @login.user_loader
    def load_user(id):
        return User.query.get(int(id))
        

##################################Student



####################################### Teacher ==> should be inherited from User but i didnt find a technical way to do it. 
class Teacher(db.Model):
	id = db.Column(db.Integer, primary_key=True)
	first_name = db.Column('first_name', db.String(20), index=True)
	last_name = db.Column('last_name', db.String(20), index=True)
	birth_date = db.Column(db.DateTime, nullable = False)

	email = db.Column('email',db.String(50),unique=True , index=True)
	registered_on = db.Column('registered_on' , db.DateTime) 
	
	profetional = db.Column(db.String(140), nullable=True)
	
	selected = db.Column(db.Boolean)
	hide = db.Column(db.Boolean)

	students = db.relationship("Role", back_populates="teacher", cascade="all, delete")
	
	def __init__(self , id, first_name, last_name, birth_date, profetional, email):
		self.id = id
		self.first_name = first_name
		self.last_name = last_name	
		self.birth_date = birth_date

		self.profetional = profetional
		self.email = email
		self.registered_on = datetime.utcnow()
		self.selected = False
		self.hide = False

		
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


####################################### Accupation 
class Accupation(db.Model):
    id = db.Column(db.Integer, primary_key=True)

    title = db.Column(db.String(140))
    body = db.Column(db.String(400))
        
    selected = db.Column(db.Boolean)
    hide = db.Column(db.Boolean)

    def __init__(self, title, body, author_id):
        self.title = title
        self.body = body
        self.author_id = author_id
        self.selected = False
        self.hide = False
####################################### Accupation


	 
############################################ Profile 	 
class Profile(db.Model):
	id = db.Column(db.Integer, primary_key = True)
	author_id = db.Column(db.Integer, db.ForeignKey('user.id'))
	title = db.Column(db.String(140), nullable=True)
	body = db.Column(db.String(400))
	timestamp = datetime.utcnow()
	selected = db.Column(db.Boolean)
	strengthes=db.relationship('Strength', secondary=profile_strength_relationships, backref='profile', cascade="all, delete"  )  
	weaknesses=db.relationship('Weakness', secondary=profile_weakness_relationships, backref='profile', cascade="all, delete" )	  
	subjects=db.relationship('Subject',    secondary=profile_subject_relationships,  backref='profile', cascade="all, delete"  )
	 
	def __init__(self ,title, body):
		self.title = title
		self.body = body
		#self.author_id = author_id
		self.timestamp = datetime.utcnow()
		self.selected = False
	 
	def add(self,profile):
		db.session.add(profile)
		return session_commit()

	def update(self):
		return session_commit()

	def delete(self,student):
		db.session.delete(profile)
		return session_commit()		  
############################################ Profile 


########################################## File

resource_ufile_relationships=db.Table('resource_ufile_relationships',
                           db.Column('resource_id', db.Integer,db.ForeignKey('resource.id')),                           
                           db.Column('ufile_id',    db.Integer,db.ForeignKey('ufile.id'))    
                           )
                           
document_ufile_relationships=db.Table('document_ufile_relationships',
                           db.Column('document_id', db.Integer,db.ForeignKey('document.id')),                           
                           db.Column('ufile_id',    db.Integer,db.ForeignKey('ufile.id'))    
                           )
							   
class Ufile(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    author_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    name = db.Column(db.String(300), nullable=True)
    data = db.Column(db.LargeBinary)   #file content
    body = db.Column(db.String(255), nullable=True) 
    selected = db.Column(db.Boolean)
    hide = db.Column(db.Boolean)

    def __init__(self, name, data, author_id):

        self.name = name
        self.data = data
        self.author_id = author_id
        self.hide = False
        self.selected = False


############################################ File  

########################################## Resource
goal_resource_relationships=db.Table('goal_resource_relationships',
                           db.Column('goal_id', db.Integer,db.ForeignKey('goal.id')),                           
                           db.Column('resource_id', db.Integer,db.ForeignKey('resource.id'))    
                           )
						   			   
class Resource(db.Model):
	id = db.Column(db.Integer, primary_key=True)
	title = db.Column(db.String(140), nullable=True)
	body = db.Column(db.String(255), nullable=True)
	selected = db.Column(db.Boolean)
	files=db.relationship('Ufile', secondary=resource_ufile_relationships, backref='resource',  single_parent=True, cascade="all, delete-orphan") 

	students = db.relationship("Std_resource", back_populates="resource", cascade="all, delete")

	def __init__(self, title, body):	
		self.title=title	
		self.body=body
		self.selected=False
############################################ Resource  



########################################## Resource

std_document_relationships=db.Table('std_document_relationships',
                           db.Column('student_id',  db.Integer,db.ForeignKey('student.id')),                           
                           db.Column('document_id', db.Integer,db.ForeignKey('document.id'))    
                           )
						   			   
class Document(db.Model):
	id = db.Column(db.Integer, primary_key=True)
	title = db.Column(db.String(140), nullable=True)
	body = db.Column(db.String(255), nullable=True)
	selected = db.Column(db.Boolean)
	files=db.relationship('Ufile', secondary=document_ufile_relationships, backref='document',  single_parent=True, cascade="all, delete-orphan") 

	students = db.relationship("Std_document", back_populates="document", cascade="all, delete")

	def __init__(self, title, body):	
		self.title=title	
		self.body=body
		self.selected=False
############################################ Resource  



########################################## goal option 

class Goal(db.Model):
    #__tablename__ = 'goals'
    id = db.Column(db.Integer, primary_key = True)
    
    dst_id =  db.Column(db.Integer, db.ForeignKey('destination.id')) 

    author_id = db.Column(db.Integer, db.ForeignKey('user.id'))

    title = db.Column(db.String(140), nullable=True)
    body =  db.Column(db.String(400))

    timestamp = datetime.utcnow()

    selected = db.Column(db.Boolean)
    hide =     db.Column(db.Boolean)

    students = db.relationship("Std_goal", back_populates="goal", cascade="all, delete")
    
    def __init__(self ,title, body, author_id, dst_id):
        self.title = title
        self.body = body
        self.author_id = author_id
        self.dst_id = dst_id
        self.timestamp = datetime.utcnow()
        self.selected = False
        self.hide = False
############################################ Goal      


### FROM https://stackoverflow.com/questions/44242802/python-flask-validate-selectfield
class Goal_form(FlaskForm):
 
    goal_title = TextField("כותרת יעד",[validators.Required("יש להכניס יעד")])                                   
    goal_body =  TextField("תאור יעד", render_kw={"rows": 70, "cols": 11})

    dst_title = TextField("כותרת מטרה",[validators.Required("יש להכניס מטרה")])                                   
    dst_body =  TextField("תאור מטרה", render_kw={"rows": 70, "cols": 11})
        
    submit = SubmitField("שמור יעד")

############################################ Goal Form for cascade dropdown display     




############################################ Destination     
 
class Destination(db.Model):
    id = db.Column(db.Integer, primary_key = True)
    author_id = db.Column(db.Integer, db.ForeignKey('user.id'))

    title = db.Column(db.String(255), nullable=False)
    body = db.Column(db.String(400))

    timestamp = datetime.utcnow()
    selected = db.Column(db.Boolean)
    hide = db.Column(db.Boolean) 

    students = db.relationship("Std_destination", back_populates="destination", cascade="all, delete")

    tags = db.relationship('Dst_Tag', back_populates="destination", cascade="all, delete")

    goals =    db.relationship('Goal', cascade='all,delete', backref='destination') # one to many


    age_range_id = db.Column(db.Integer, db.ForeignKey('age_range.id'), nullable=True) 
    scrt_id =  db.Column(db.Integer, db.ForeignKey('scrt.id'),          nullable=True) 


    def __init__(self ,title, body, author_id):
        self.title = title
        self.body = body

        self.author_id = author_id
        self.timestamp = datetime.utcnow()
        self.selected = False
        self.hide = False
        
    def add(self,destination):
        db.session.add(destination)
        return session_commit()

    def update(self):
        return session_commit()

    def delete(self,destination):
        db.session.delete(destination)
        return session_commit()
        
    def __repr__(self):
        return '<Dst %r>' % self.title
    
############################################ Destination


### FROM https://stackoverflow.com/questions/44242802/python-flask-validate-selectfield
class Dst_form(FlaskForm):
    ar =   SelectField('קבוצת גיל', choices=[], validators=[validators.Required(message=('יש לבחור קבוצת גיל'))], coerce=int)                      
    tag =  SelectField('נושא',      choices=[], validators=[validators.Required(message=('יש לבחור נושא'))], coerce=int)
    scrt = SelectField('רמת אבטחה', choices=[], validators=[validators.Required(message=('יש לבחור רמת אבטחה'))], coerce=int)
    
    dst_title = TextField("כותרת מטרה",[validators.Required("יש להכניס מטרה")])                                   
    dst_body =  TextField("תאור מטרה", render_kw={"rows": 70, "cols": 11})
    
    submit = SubmitField("שמור מטרה")
    
    ### FROM https://stackoverflow.com/questions/44242802/python-flask-validate-selectfield
    def validate_ar(form):
        if  not form.ar.data == None:
          raise ValidationError('יש לבחור קבוצת גיל')

############################################ Dst Form for cascade dropdown display     


# from https://github.com/Leo-G/Freddy/blob/master/app/models.py		  
#Universal functions

def  session_commit ():
	try:
		db.session.commit()
	except SQLAlchemyError as e:
		db.session.rollback()
		reason=str(e)
		return reason
