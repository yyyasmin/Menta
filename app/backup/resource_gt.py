				 
########################################## General_choice_resource			   

class General_choice_resource(db.Model):

    #FROM https://stackoverflow.com/questions/40521770/why-am-i-getting-sqlalchemy-error-table-args-value-must-be-a-tuple-dict-o
    __table_args__ = (db.UniqueConstraint('general_choice_id', 'resource_id', name='general_choice_resource_pk'), )
    #FROM http://docs.sqlalchemy.org/en/rel_0_9/orm/basic_relationships.html#association-object 
        
    general_choice_id = db.Column(db.Integer,    db.ForeignKey('general_choice.id'),    primary_key=True)
    resource_id = db.Column(db.Integer, db.ForeignKey('resource.id'), primary_key=True)

    title = db.Column(db.String(140))
    selected = db.Column(db.Boolean)
    hide = db.Column(db.Boolean)

    #FROM http://docs.sqlalchemy.org/en/latest/orm/basic_relationships.html#association-object
    resource = db.relationship("Resource", back_populates="general_choices")
    
    general_choice = db.relationship("General_choice",       back_populates="resources")
    
    def __init__(self, general_choice_id, resource_id):
        self.general_choice_id=general_choice_id
        self.resource_id=resource_id
        self.selected=False
        self.hide = False
    
############################################ General_choice_resource

