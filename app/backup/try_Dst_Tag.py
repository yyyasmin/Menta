########################################## Dst Tag			   
class Dst_Tag(db.Model):

	#FROM https://stackoverflow.com/questions/40521770/why-am-i-getting-sqlalchemy-error-table-args-value-must-be-a-tuple-dict-o
	__table_args__ = (db.UniqueConstraint('destination_id', 'tag_id', name='destination_tag_pk'), )
	#FROM http://docs.sqlalchemy.org/en/rel_0_9/orm/basic_relationships.html#association-object 
	#id = db.Column(db.Integer, primary_key=True)
		
	destination_id = db.Column(db.Integer, db.ForeignKey('destination.id'), primary_key=True)
	tag_id =    db.Column(db.Integer, db.ForeignKey('tag.id'),    primary_key=True)
	
	title = db.Column(db.String(140), nullable=True)
	selected = db.Column(db.Boolean)
	status = db.Column(db.String(100), nullable=False)
	
	#FROM http://docs.sqlalchemy.org/en/latest/orm/basic_relationships.html#association-object
	tag = db.relationship("Tag", back_populates="destinations")
	destination = db.relationship("Destination", back_populates="tags")

	def __init__(self, destination_id, tag_id):
		self.destination_id=destination_id
		self.tag_id=tag_id
		self.selected=False
############################################ Dst Tag