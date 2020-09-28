
########################################## Std_general_txt 			   
class Std_general_txt(db.Model):

    #FROM https://stackoverflow.com/questions/40521770/why-am-i-getting-sqlalchemy-error-table-args-value-must-be-a-tuple-dict-o

    __table_args__ = (db.UniqueConstraint('student_id', 'general_txt_id', name='student_general_txt_pk'), )

    student_id = db.Column(db.Integer,     db.ForeignKey('student.id'),      primary_key=True)
    general_txt_id = db.Column(db.Integer, db.ForeignKey('general_txt.id'),  primary_key=True)   

    timestamp = datetime.utcnow()
    
    due_date = db.Column(db.Date)
    status_id = db.Column(db.Integer, db.ForeignKey('status.id')) 
    acc_id = db.Column(db.Integer,    db.ForeignKey('accupation.id')) 
    scrt_id = db.Column(db.Integer,   db.ForeignKey('scrt.id'))
    
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

    def is_editable(self, user_id):
        return (user_id == self.general_txt.author_id)
        
    def set_editable(self, user_id):
        #############import pdb;  pdb.set_trace()
        if  (user_id == self.general_txt.author_id):
            editable = True
        return editable
        
        
############################################ Std_general_txt
