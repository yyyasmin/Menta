
########################################## Std_resource 			   
class Std_resource(db.Model):

	#FROM https://stackoverflow.com/questions/40521770/why-am-i-getting-sqlalchemy-error-table-args-value-must-be-a-tuple-dict-o

	__table_args__ = (db.UniqueConstraint('student_id', 'resource_id', name='student_resource_pk'), )

	#FROM http://docs.sqlalchemy.org/en/rel_0_9/orm/basic_relationships.html#association-object 
	#id = db.Column(db.Integer, primary_key=True)


    student_id = db.Column(db.Integer,  db.ForeignKey('student.id'),      primary_key=True)
    resource_id = db.Column(db.Integer, db.ForeignKey('resource.id'), primary_key=True)
 
    dst_id =  db.Column(db.Integer,  db.ForeignKey('destination.id'))
    goal_id = db.Column(db.Integer,   db.ForeignKey('goal.id')) 
    
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

