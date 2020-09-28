
####################################### User

class User(db.Model):
	id = db.Column(db.Integer, primary_key=True)
	username = db.Column('username', db.String(20), unique=True , index=True)
	password = db.Column('password' , db.String(10))
	email = db.Column('email',db.String(50),unique=True , index=True)

    students = db.relationship("User_data_permission",     back_populates="user", cascade="all, delete")
    teachers =  db.relationship("User_data_permission",    back_populates="user", cascade="all, delete")
    general_txts = db.relationship("User_data_permission", back_populates="user", cascade="all, delete, delete-orphan")
    resources = db.relationship("User_data_permission",    back_populates="user", cascade="all, delete, delete-orphan")


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



########################################## Std_general_txt 			   
class User_data_permission(db.Model):

    #FROM https://stackoverflow.com/questions/40521770/why-am-i-getting-sqlalchemy-error-table-args-value-must-be-a-tuple-dict-o

    __table_args__ = (db.UniqueConstraint('student_id', 'general_txt_id', name='student_general_txt_pk'), )

    user_id = db.Column(db.Integer, db.ForeignKey('student.id'), primary_key=True)
    
    general_txt_id = db.Column(db.Integer, db.ForeignKey('general_txt.id'))   

    timestamp = datetime.utcnow()
    
    students = db.relationship("User_data_permission",       back_populates="general_txt", cascade="all, delete")
    teachers =  db.relationship("User_data_permission",                     back_populates="student", cascade="all, delete")
    general_txts = db.relationship("User_data_permission",       back_populates="student", cascade="all, delete, delete-orphan")
    resources = db.relationship("User_data_permission",             back_populates="student", cascade="all, delete, delete-orphan")
 
    editable = db.Column(db.Boolean)
    
    selected = db.Column(db.Boolean)
    hide =     db.Column(db.Boolean)


    #FROM http://docs.sqlalchemy.org/en/latest/orm/basic_relationships.html#association-object
    general_txt = db.relationship("General_txt", back_populates="students")
    student =     db.relationship("Student",     back_populates="general_txts")

    def __init__(self, student_id, general_txt_id):
        self.student_id=student_id
        self.general_txt_id=general_txt_id
        self.selected=False
        self.hide=False
    
############################################ Std_general_txt
