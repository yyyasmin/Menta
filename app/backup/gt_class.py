
class General_txt(db.Model):
   
    id = db.Column(db.Integer, primary_key=True)
            
    author_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    
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

    children = db.relationship(
            'General_txt', secondary=parent_child_relationship,
            primaryjoin=(parent_child_relationship.c.parent_id == id),
            secondaryjoin=(parent_child_relationship.c.child_id == id),
            backref=db.backref('parent_child_relationship', lazy='dynamic'),
            lazy='dynamic')
            
   #FROM http://docs.sqlalchemy.org/en/latest/orm/basic_relationships.html#association-object
    
    students = db.relationship("Std_general_txt",       back_populates="general_txt", cascade="all, delete")         
    files =    db.relationship("Ufile_general_txt", back_populates="general_txt", cascade="all, delete")

#FROM  Inheritance https://github.com/pallets/flask-sqlalchemy/issues/479
            
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
        return self.children.filter(
            parent_child_relationship.c.child_id == general_txt.id).count() > 0
            
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
    