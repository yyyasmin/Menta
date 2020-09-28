

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
    tag = db.relationship("Tag", back_populates="students")
    student =     db.relationship("Student",     back_populates="tags")

    def __init__(self, student_id, tag_id):
        self.student_id=student_id
        self.tag_id=tag_id
        self.selected=False
        self.hide=False

############################################ Std_tag


