class Sub_tag(General_txt):
    __tablename__ = 'sub_tag'

    __mapper_args__ = {'polymorphic_identity': 'sub_tag'}

    id = db.Column(db.ForeignKey(General_txt.id), primary_key=True)
    
    def __init__(self, title, body, author_id):
                         
        self.h_name = 'תת נושא'   
        self.e_name = 'Sub tag'  
        
        self.class_name = 'Sub_tag'
        self.gt_type = 'Sub_tag'
        
        self.color_txt = 'black'
        self.color = '#00284d'
        self.editable = True     
        super(self.__class__, self).__init__(title, body, author_id)
   