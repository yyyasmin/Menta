
########################################## Resource
						   			   
class Resource(db.Model):

    id = db.Column(db.Integer, primary_key=True)

    type = db.Column(db.String(50))
    
    author_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    
    h_name = db.Column(db.String(50))   # for example" 'חוזקה'
    e_name = db.Column(db.String(50))   # for example" 'Are of Subject'
    
    gt_type = db.Column(db.String(50))  # for example" 'Subject'
    class_name = db.Column(db.String(50))  # for example" 'Subject'
    
    title = db.Column(db.String(255), nullable=False)
    body = db.Column(db.String(400))
    
    color_txt = db.Column(db.String(10))
    color = db.Column(db.String(10))
   
    default = db.Column(db.Boolean)         
    selected = db.Column(db.Boolean)
    hide = db.Column(db.Boolean)

    files=db.relationship('Ufile', secondary=resource_ufile_relationships, backref='resource',  single_parent=True, cascade="all, delete-orphan") 

    students = db.relationship("Std_resource",                   back_populates="resource", cascade="all, delete")
    general_txts = db.relationship("General_txt_resource",       back_populates="resource", cascade="all, delete")
            
    __mapper_args__ = {
        'polymorphic_identity':'resource',
        'polymorphic_on':type
    }

    def __init__(self, title, body, author_id):	
        self.title=title	
        self.body=body
        self.author_id=author_id
        
        self.selected=False
        self.hide=False
        self.default=False
        
############################################ Resource  

class Document(Resource):
    __tablename__ = 'document'

    __mapper_args__ = {'polymorphic_identity': 'type'}

    id = db.Column(db.ForeignKey(Resource.id), primary_key=True)
    def __init__(self, title, body, author_id):
    
        h_name = 'מסמכים'   
        e_name = 'Document'  
            
        class_name = 'Document'
        gt_type = 'Document'
        
        color_txt = 'black'
        color = '#00284d'
        editable = True     
        super(self.__class__, self).__init__(title, body, author_id)
    

