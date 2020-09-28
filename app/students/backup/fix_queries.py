 children = db.relationship(
            'General_txt', secondary=parent_child_relationship,
            primaryjoin=(parent_child_relationship.c.parent_id == id),
            secondaryjoin=(parent_child_relationship.c.child_id == id),
            backref=db.backref('parent_child_relationship', lazy=False),
            lazy=False)
			
def is_parent_of(self, general_txt):
        return general_txt in self.children