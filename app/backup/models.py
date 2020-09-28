
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

### For Inheritance
from sqlalchemy.ext.declarative import declared_attr, has_inherited_table


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

import json
from time import time
            
            
#FROM https://blog.miguelgrinberg.com/post/the-flask-mega-tutorial-part-xxi-user-notifications            
class Notification(db.Model):

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(128), index=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    #timestamp = db.Column(db.DateTime, index=True, default=datetime.utcnow)
    timestamp = datetime.utcnow()

    payload_json = db.Column(db.Text)

    def get_data(self):
        return json.loads(str(self.payload_json))  

class Message(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    sender_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    recipient_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    body = db.Column(db.String(140))
    #timestamp = db.Column(db.DateTime, index=True, default=datetime.utcnow)
    timestamp = datetime.utcnow()

    def __repr__(self):
        return '<Message {}>'.format(self.body)


#FROM https://github.com/miguelgrinberg/microblog/blob/v0.8/app/models.py

from datetime import datetime
from flask_login import UserMixin


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
        ################import pdb;  pdb.set_trace()
        if  (user_id == self.general_txt.author_id):
            self.editable = True
        return editable
        
        
############################################ Std_general_txt


#FROM https://github.com/miguelgrinberg/microblog/blob/v0.8/app/models.py

########################################## Parent_child_relationship

parent_child_relationship = db.Table('parent_child_relationship',
    db.Column('parent_id', db.Integer, db.ForeignKey('general_txt.id')),
    db.Column('child_id',  db.Integer, db.ForeignKey('general_txt.id'))
) 	
		   
########################################## Parent_child_relationship 
			   

############################################ General_txt 

class General_txt(db.Model):
   
    id = db.Column(db.Integer, primary_key=True)
            
    author_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    ufile_id =  db.Column(db.Integer, db.ForeignKey('ufile.id'), nullable=True)
        
    type = db.Column(db.String(50))     # for example" 'subject'
    h_name = db.Column(db.String(50))   # for example" 'חוזקה'
    e_name = db.Column(db.String(50))   # for example" 'Are of Subject'
    
    gt_type = db.Column(db.String(50))  # for example" 'Subject'
    class_name = db.Column(db.String(50))  # for example" 'Subject'
    
    title = db.Column(db.String(255), nullable=False)
    body = db.Column(db.String(400))
    default = db.Column(db.Boolean)
    
    color_txt = db.Column(db.String(10))
    color = db.Column(db.String(10))
        
    timestamp = datetime.utcnow()
    
    selected = db.Column(db.Boolean)
    hide = db.Column(db.Boolean) 

    '''
    children = db.relationship(
            'General_txt', secondary=parent_child_relationship,
            primaryjoin=(parent_child_relationship.c.parent_id == id),
            secondaryjoin=(parent_child_relationship.c.child_id == id),
            backref=db.backref('parent_child_relationship', lazy='dynamic'),
            lazy='dynamic')
    '''
    
    #Anthony's suggestion
            
    children = db.relationship(
                'General_txt', secondary=parent_child_relationship,
                primaryjoin=(parent_child_relationship.c.parent_id == id),
                secondaryjoin=(parent_child_relationship.c.child_id == id),
                backref=db.backref('parent_child_relationship', lazy=False),
                lazy=False) 
                
    students = db.relationship("Std_general_txt",   back_populates="general_txt", cascade="all, delete")
                        
    __mapper_args__ = {
        'polymorphic_identity':'general_txt',
        'polymorphic_on':type
    }
        
    def set_parent(self, general_txt):
        if not self.is_parent_of(general_txt):
            self.children.append(general_txt)

    def unset_parent(self, general_txt):
        if self.is_parent_of(general_txt):
            self.children.remove(general_txt)
            
    def is_parent_of(self, general_txt):
        return general_txt in self.children
            
    '''
    def is_parent_of(self, general_txt):
        return self.children.filter(
            parent_child_relationship.c.child_id == general_txt.id).count() > 0
    '''
    
    def children_ids(self):
            return General_txt.query.join(
                parnet_child_relationship, (parnet_child_relationship.c.children_id == General_txt.id)).filter(
                    parnet_child_relationship.c.parent_id == self.id).order_by(
                        Generl_txt.title) 
                        
    def get_all_gts_of_type(self):
        return eval(self.gt_type).query.all()
                                
    def __init__(self ,title, body, author_id):
        self.title = title
        self.body = body
        
        self.author_id = author_id

        self.timestamp = datetime.utcnow()        
        self.due_date = datetime.today()

        self.selected = False
        self.hide = False
        self.default = False
        
    def __repr__(self):
        return '<Dst %r>' % self.title
                                
############################################ General_txt

class Gt_form(FlaskForm):
      

    tag =  SelectField('נושא', choices=[], validators=[validators.Required(message=('יש לבחור נושא'))], coerce=int)
    ar =  SelectField('קבוצת גיל', choices=[], validators=[validators.Required(message=('יש לבחור קבוצת גיל'))], coerce=int)
    scrt =  SelectField('רמת אבטחה', choices=[], validators=[validators.Required(message=('יש לבחור רמת אבטחה'))], coerce=int)

    gt_type = StringField('Profile category')
    gt_type_txt = StringField('קטגורית פרופיל')
    
    gt_color_txt = StringField('צבע')
    gt_color = StringField('color')
      
    gt_title = TextField("הטקסט",[validators.Required("יש להכניס כותרת")])                                   
    gt_body =  TextField("תאור", render_kw={"rows": 70, "cols": 11})
     
    sbj_title = TextField("תחום עיניין",[validators.Required("יש להכניס תחום עיניין")])                                   
    sbj_body =  TextField("תאור תחום עיניין", render_kw={"rows": 70, "cols": 11})
    
    strn_title = TextField("חוזקה",[validators.Required("יש להכניס חוזקה")])                                   
    strn_body =  TextField("תאור חוזקה", render_kw={"rows": 70, "cols": 11})
    
    weak_title = TextField("חולשה",[validators.Required("יש להכניס חולשה")])                                   
    weak_body =  TextField("תאור חולשה", render_kw={"rows": 70, "cols": 11})

    gt_title = TextField("כותרת מטרה",[validators.Required("יש להכניס מטרה")])                                   
    gt_body =  TextField("תאור מטרה", render_kw={"rows": 70, "cols": 11})

    goal_title = TextField("כותרת יעד",[validators.Required("יש להכניס יעד")])                                   
    goal_body =  TextField("תאור יעד", render_kw={"rows": 70, "cols": 11})

    title = TextField("כותרת משימה",[validators.Required("יש להכניס מטרה")])                                   
    body =  TextField("תאור משימה", render_kw={"rows": 70, "cols": 11})

    
    who = SelectField('תפקיד מבצע המשימה', choices=[], validators=[validators.Required(message=('יש לבחור מבצע למשימה'))])
    status = SelectField('סטאטוס ביצוע', choices=[],   validators=[validators.Required(message=('יש לבחור סטאטוס ביצוע'))])
    due_date =  DateField('due_date')
          
    submit = SubmitField("שמור")
    
    ### FROM https://stackoverflow.com/questions/44242802/python-flask-validate-selectfield
    def validate_tag(form):
        if not form.tag.data == None:
          raise ValidationError('יש לבחור נושא')
          
############ General_txt Inherited classes #################

class School(General_txt):
    __tablename__ = 'school'
    __mapper_args__ = {'polymorphic_identity': 'school'}
    id = db.Column(db.ForeignKey(General_txt.id), primary_key=True)
    
    def __init__(self ,title, body, author_id):
        
        self.h_name = 'בית ספר'   
        self.e_name = 'School'  
     
        self.class_name = 'School'
        self.gt_type = 'School'
        self.color_txt = 'black'
        self.color = '##000066'  
        self.editable = True
        super(self.__class__, self).__init__(title, body, author_id)       
            
  
class Destination(General_txt):
    __tablename__ = 'destination'
    __mapper_args__ = {'polymorphic_identity': 'destination'}
    id = db.Column(db.ForeignKey(General_txt.id), primary_key=True)
    
    def __init__(self ,title, body, author_id):
        self.h_name = "מטרה"   # for example" 'חוזקה'
        self.e_name = 'Destination'   # for example" 'subect' 
        self.class_name = 'Destination'
        self.gt_type = 'Destination'
        
        self.color_txt = 'black'
        self.color = '##000066'  
        self.editable = True
        super(self.__class__, self).__init__(title, body, author_id)       
            
### FROM https://stackoverflow.com/questions/44242802/python-flask-validate-selectfield
class Dst_form(FlaskForm):
    ar =   SelectField('קבוצת גיל', choices=[], validators=[validators.Required(message=('יש לבחור קבוצת גיל'))], coerce=int)                      
    tag =  SelectField('נושא',      choices=[], validators=[validators.Required(message=('יש לבחור נושא'))], coerce=int)
    scrt = SelectField('רמת אבטחה', choices=[], validators=[validators.Required(message=('יש לבחור רמת אבטחה'))], coerce=int)
    
    gt_title = TextField("כותרת מטרה",[validators.Required("יש להכניס מטרה")])                                   
    gt_body =  TextField("תאור מטרה", render_kw={"rows": 70, "cols": 11})
    
    submit = SubmitField("שמור מטרה")
    
    ### FROM https://stackoverflow.com/questions/44242802/python-flask-validate-selectfield
    def validate_ar(form):
        if  not form.ar.data == None:
          raise ValidationError('יש לבחור קבוצת גיל')

############################################ Dst Form for cascade dropdown display     
    

class Goal(General_txt):
    __tablename__ = 'goal'
    __mapper_args__ = {'polymorphic_identity': 'goal'}
    id = db.Column(db.ForeignKey(General_txt.id), primary_key=True)
    
    def __init__(self ,title, body, author_id):        
        
        self.h_name = 'יעד'   
        self.e_name = 'Goal'  
          
        self.class_name = 'Goal'
        self.gt_type = 'Goal'
        self.color_txt = 'black'
        self.color = '##000066'  
        self.editable = True
        super(self.__class__, self).__init__(title, body, author_id)       
            

### FROM https://stackoverflow.com/questions/44242802/python-flask-validate-selectfield
class Goal_form(FlaskForm):
 
    goal_title = TextField("כותרת יעד",[validators.Required("יש להכניס יעד")])                                   
    goal_body =  TextField("תאור יעד", render_kw={"rows": 70, "cols": 11})

    gt_title = TextField("כותרת מטרה",[validators.Required("יש להכניס מטרה")])                                   
    gt_body =  TextField("תאור מטרה", render_kw={"rows": 70, "cols": 11})
        
    submit = SubmitField("שמור יעד")

############################################ Goal Form for cascade dropdown display     


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

    
class Todo(General_txt):
    __tablename__ = 'todo'
    __mapper_args__ = {'polymorphic_identity': 'todo'}
    id = db.Column(db.ForeignKey(General_txt.id), primary_key=True)
    
    def __init__(self ,title, body, author_id):
        
        self.h_name = 'משימה'   
        self.e_name = 'Mission'  

        self.class_name = 'Todo'
        self.gt_type = 'Todo'
        self.color_txt = 'black'
        self.color = '##000066'  
        self.editable = True
        super(self.__class__, self).__init__(title, body, author_id)       
            


############################################ Todo_form
#FROM https://stackoverflow.com/questions/7979548/how-to-render-my-textarea-with-wtforms
########################################## Todo     
class Todo_form(FlaskForm):
    id = db.Column(db.Integer, primary_key=True)
    
    dst_id =  db.Column(db.Integer, db.ForeignKey('destination.id'))
    goal_id =  db.Column(db.Integer, db.ForeignKey('goal.id'))

    title = TextField("כותרת משימה",[validators.Required("יש להכניס מטרה")])                                   
    body =  TextField("תאור משימה", render_kw={"rows": 70, "cols": 11})
    
    who = SelectField('תפקיד מבצע המשימה', choices=[], validators=[validators.Required(message=('יש לבחור מבצע למשימה'))])
    status = SelectField('סטאטוס ביצוע', choices=[],   validators=[validators.Required(message=('יש לבחור סטאטוס ביצוע'))])
    due_date =  DateField('due_date')

    selected = db.Column(db.Boolean)
    hide =     db.Column(db.Boolean)
    
    submit = SubmitField("שמור משימה")	
    
############################################ Todo_form

    
class Profile(General_txt):
    __tablename__ = 'profile'
    __mapper_args__ = {'polymorphic_identity': 'profile'}
    id = db.Column(db.ForeignKey(General_txt.id), primary_key=True)
    #FROM https://stackoverflow.com/questions/25189017/tablemodel-inheritance-with-flask-sqlalchemy
    
    def __init__(self ,title, body, author_id):
                
        self.h_name = 'פרופיל'   
        self.e_name = 'Profile'  

        self.class_name = 'Profile'
        self.gt_type = 'Profile'
        
        self.color_txt = 'black'
        self.color = '##000066'  
        self.editable = True
        super(self.__class__, self).__init__(title, body, author_id)       
            

class Prf_form(FlaskForm):
    tag =  SelectField('נושא', choices=[], validators=[validators.Required(message=('יש לבחור נושא'))], coerce=int)
    
    sbj_title = TextField("תחום עיניין",[validators.Required("יש להכניס תחום עיניין")])                                   
    sbj_body =  TextField("תאור תחום עיניין", render_kw={"rows": 70, "cols": 11})
    
    strn_title = TextField("תחום עיניין",[validators.Required("יש להכניס חוזקה")])                                   
    strn_body =  TextField("תאור תחום עיניין", render_kw={"rows": 70, "cols": 11})
    
    weak_title = TextField("תחום עיניין",[validators.Required("יש להכניס חולשה")])                                   
    weak_body =  TextField("תאור תחום עיניין", render_kw={"rows": 70, "cols": 11})
      
    submit = SubmitField("שמור")
    
    ### FROM https://stackoverflow.com/questions/44242802/python-flask-validate-selectfield
    def validate_tag(form):
        if not form.tag.data == None:
          raise ValidationError('יש לבחור נושא')

class Strength(General_txt):
    __tablename__ = 'strength'
    __mapper_args__ = {'polymorphic_identity': 'strength'}
    id = db.Column(db.ForeignKey(General_txt.id), primary_key=True)
    
    def __init__(self ,title, body, author_id):
        
        self.h_name = 'חוזקה'   
        self.e_name = 'Strenght'  

        self.class_name = 'Strength'
        self.gt_type = 'Strength'
        
        self.color_txt = 'green'
        self.color = '#66ff99'  
        self.editable = True
        super(self.__class__, self).__init__(title, body, author_id)       
            
class Subject(General_txt):
    __tablename__ = 'subject'
    __mapper_args__ = {'polymorphic_identity': 'subject'}
    id = db.Column(db.ForeignKey(General_txt.id), primary_key=True)
          
    def __init__(self ,title, body, author_id):
                 
        self.h_name = 'תחום עיניין'   
        self.e_name = 'Subject'  
       
        self.class_name = 'Subject'
        self.gt_type = 'Subject'
        
        self.color_txt = 'blue'
        self.color = '#3366ff' 
        self.editable = True        
        super(self.__class__, self).__init__(title, body, author_id)

class Weakness(General_txt):
    __tablename__ = 'weakness'
    __mapper_args__ = {'polymorphic_identity': 'weakness'}
    id = db.Column(db.ForeignKey(General_txt.id), primary_key=True)
    
    def __init__(self ,title, body, author_id):
                 
        self.h_name = 'חולשה'   
        self.e_name = 'Weakness'  
               
        self.class_name = 'Weakness'
        self.gt_type = 'Weakness'
        
        self.color_txt = 'red'
        self.color = '#ff9999'
        self.editable = True         
        super(self.__class__, self).__init__(title, body, author_id)

   
##########Choices #####################################

class Tag(General_txt):
    __tablename__ = 'tag'

    __mapper_args__ = {'polymorphic_identity': 'tag'}

    id = db.Column(db.ForeignKey(General_txt.id), primary_key=True)
    
    def __init__(self, title, body, author_id):
                         
        self.h_name = 'נושא'   
        self.e_name = 'Tag'  
        
        self.class_name = 'Tag'
        self.gt_type = 'Tag'
        
        self.color_txt = 'black'
        self.color = '#00284d'
        self.editable = True     
        super(self.__class__, self).__init__(title, body, author_id)
      
class Age_range(General_txt):

    __tablename__ = 'age_range'

    __mapper_args__ = {'polymorphic_identity': 'age_range'}

    id = db.Column(db.ForeignKey(General_txt.id), primary_key=True)
     
    from_age = db.Column(db.Integer)
    to_age = db.Column(db.Integer)
         
    def __init__(self, title, body, from_age, to_age, author_id):
        self.from_age = from_age
        self.to_age = to_age
                         
        self.h_name = 'קבוצת גיל'   
        self.e_name = 'Age range'  
                
        self.class_name = 'Age_range'
        self.gt_type = 'Age_range'
        
        self.color_txt = 'black'
        self.color = '#00284d'
        self.editable = True         
        super(self.__class__, self).__init__(title, body, author_id)
        
class Scrt(General_txt):

    __tablename__ = 'scrt'
    __mapper_args__ = {'polymorphic_identity': 'scrt'}

    id = db.Column(db.ForeignKey(General_txt.id), primary_key=True)
    
    def __init__(self, title, body, author_id):
        
        self.h_name = 'רמת אבטחה'   
        self.e_name = 'Security level'  
                
        self.class_name = 'Scrt'
        self.gt_type = 'Scrt'
        
        self.color_txt = 'black'
        self.color = '#00284d'
        self.editable = True     
        super(self.__class__, self).__init__(title, body, author_id)
     
      
class Status(General_txt):

    __tablename__ = 'status'
    __mapper_args__ = {'polymorphic_identity': 'status'}
    
    id = db.Column(db.ForeignKey(General_txt.id), primary_key=True)
    
    #color = db.Column(db.String(10))
    
    def __init__(self, title, body, author_id):
           
        self.h_name = 'סטאטוס'   
        self.e_name = 'Status'  
                
        self.class_name = 'Status'
        self.gt_type = 'Status'
        
        self.color_txt = 'black'
        self.color = '#00284d'
        self.editable = True     
        super(self.__class__, self).__init__(title, body, author_id)

    
class Accupation(General_txt):

    __tablename__ = 'accupation'
    __mapper_args__ = {'polymorphic_identity': 'accupation'}
       
    id = db.Column(db.ForeignKey(General_txt.id), primary_key=True)
    
    def __init__(self, title, body, author_id):
    
        self.h_name = 'תפקיד'   
        self.e_name = 'Accupation'  
            
        self.class_name = 'Accupation'
        self.gt_type = 'Accupation'
        
        self.color_txt = 'black'
        self.color = '#00284d'
        self.editable = True     
        super(self.__class__, self).__init__(title, body, author_id)
    
##########Choices #####################################


########################################## Resource
						   			   
class Resource(General_txt):

    __tablename__ = 'resource'
    __mapper_args__ = {'polymorphic_identity': 'resource'}
       
    id = db.Column(db.ForeignKey(General_txt.id), primary_key=True)
    
    def __init__(self, title, body, author_id):
    
        self.h_name = 'מקורות'   
        self.e_name = 'Resource'  
            
        self.class_name = 'Resource'
        self.gt_type = 'Resource'
        
        self.color_txt = 'black'
        self.color = '#00284d'
        self.editable = True     
        super(self.__class__, self).__init__(title, body, author_id)
   

class Document(General_txt):

    __tablename__ = 'document'
    __mapper_args__ = {'polymorphic_identity': 'document'}
       
    id = db.Column(db.ForeignKey(General_txt.id), primary_key=True)
    
    def __init__(self, title, body, author_id):
    
        self.h_name = 'מסמך'   
        self.e_name = 'Document'  
            
        self.class_name = 'Document'
        self.gt_type = 'Document'
        
        self.color_txt = 'black'
        self.color = '#00284d'
        self.editable = True     
        super(self.__class__, self).__init__(title, body, author_id)

############################################ Document  

  
########################################## U-File
                           						   
class Ufile(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    author_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    
    data = db.Column(db.LargeBinary)   #file content
    
    name = db.Column(db.String(300), nullable=True)
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

 		
##################################Student													
class Student(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    first_name = db.Column('first_name', db.String(20))
    last_name = db.Column('last_name', db.String(20), index=True)
    birth_date = db.Column(db.Date, nullable = True)
    grade  = db.Column('grade', db.String(10))
    background = db.Column('background', db.String)

    author_id = db.Column(db.Integer, db.ForeignKey('user.id'))    
    timestamp = datetime.utcnow()
    registered_on = db.Column('registered_on' , db.Date) 

    selected = db.Column(db.Boolean)
    hide = db.Column(db.Boolean)

    #FROM http://docs.sqlalchemy.org/en/latest/orm/basic_relationships.html#association-object

    teachers =  db.relationship("Role",                     back_populates="student", cascade="all, delete")
    general_txts = db.relationship("Std_general_txt",       back_populates="student", cascade="all, delete, delete-orphan")

    def __init__(self, id, first_name, last_name ,birth_date, grade, author_id):
        self.id = id
        self.first_name = first_name
        self.last_name = last_name	
        self.birth_date = birth_date
        self.grade = grade
        
        self.registered_on = datetime.utcnow()
        self.author_id = author_id

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



####################################### 
class Teacher(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    first_name = db.Column('first_name', db.String(20), index=True)
    last_name = db.Column('last_name', db.String(20), index=True)
    birth_date = db.Column(db.DateTime, nullable = False)

    email = db.Column('email',db.String(50),unique=True , index=True)

    author_id = db.Column(db.Integer, db.ForeignKey('user.id'))    
    timestamp = datetime.utcnow()
    registered_on = db.Column('registered_on' , db.Date) 

    profetional = db.Column(db.String(140), nullable=True)

    selected = db.Column(db.Boolean)
    hide = db.Column(db.Boolean)

    students = db.relationship("Role", back_populates="teacher", cascade="all, delete")

    def __init__(self , id, first_name, last_name, birth_date, profetional, email, author_id):
        self.id = id
        self.first_name = first_name
        self.last_name = last_name	
        self.birth_date = birth_date

        self.profetional = profetional
        self.email = email
        
        self.registered_on = datetime.utcnow()
        self.author_id = author_id
        
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

  
  
# from https://github.com/Leo-G/Freddy/blob/master/app/models.py		  
#Universal functions

def  session_commit ():
	try:
		db.session.commit()
	except SQLAlchemyError as e:
		db.session.rollback()
		reason=str(e)
		return reason
  