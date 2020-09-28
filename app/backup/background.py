

########################################## Std_background
 			   
class Std_background(db.Model):

    #FROM https://stackoverflow.com/questions/40521770/why-am-i-getting-sqlalchemy-error-table-args-value-must-be-a-tuple-dict-o

    student_id = db.Column(db.Integer,     db.ForeignKey('student.id'), primary_key=True)
    
    background_title = db.Column(db.String(300))
    background_body =  db.Column(db.Text)

    timestamp = datetime.utcnow()

    selected = db.Column(db.Boolean)
    hide =     db.Column(db.Boolean)


    #FROM http://docs.sqlalchemy.org/en/latest/orm/basic_relationships.html#association-object
    background = db.relationship("Destination", back_populates="students")
    student =     db.relationship("Student",    back_populates="backgrounds")

    def __init__(self, student_id):
        self.student_id=student_id
        self.selected=False
        self.hide=False

############################################ Std_background

