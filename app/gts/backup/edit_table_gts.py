	
################ START studets gts ##################
	
@std.route('/edit_std_gts', methods=['GET', 'POST'])
@login_required
def edit_table_gts(Gt, Gt_sub, Gt_sub_sub, Gt_sub_sub_sub):   # for example: for student_subjects  ==> Gt = 'Subject' stored  gt.gt_type

    std = Student.query.filter(Student.selected==True).first()
    if std == None:
        flash("Please select a student first ")
        return redirect(url_for('students.edit_students'))
        
    ###########################################################
    # Get students gt of Type Gt                              #
    # If there is no one create a new one and attach to std   #
    ###########################################################
    
    std_gts = []                                             
    all_gts  = eval(Gt).query.all()                          
    for std_gt in std.general_txts:
    
        #############import pdb; pdb.set_trace()
        ##print("")
        ##print("")
        ##print("")
        ##print("std_gt.general_txt.gt_type", std_gt.general_txt.gt_type)
        ##print("GT eval ", Gt, eval(Gt))
        ##print("std_gt.general_txt.gt_type == Gt", std_gt.general_txt.gt_type == Gt)
        ##print("std_gt.general_txt.gt_type == eval(Gt)", std_gt.general_txt.gt_type == Gt)
        ##print("")
        ##print("")
        ##print("")
        
        if std_gt.general_txt.gt_type == Gt:
            std_gts.append(std_gt.general_txt)
                   
    gts_not_of_student = list(set(all_gts).difference(set(std_gts)))  #main_gts_not_of_student = all_main_gts - std_gts
    
    ##print("std_gts", std_gts)
    ##print("")
    
    # Get gt's categories
    gt_categories = []  
    for std_gt in std_gts:    
        for x in get_categories_of(std_gt):
            if x not in gt_categories:
                gt_categories.append(x)

    #################import pdb; pdb.set_trace()
    
    ##################################################################                                
    ######### Level2 -- Gt's children of Type in Categories ##########
    ##################################################################     
    gt_subs = []
    gt_subs_not_of_std=[]
    for gt in std_gts: 
        gt_subs.extend(get_gt_all_categories_children(gt))     
    gt_subs_not_of_std = get_gt_all_categories_children_not_of_std(std, gt)  #main_gts_not_of_student = all_main_gts - std_gts
    
    #'''
    #NOT OF DEBUG 
    print("gt_subs : ", gt_subs)
    print("")
    print("gt_subs_not_of_std : ",gt_subs_not_of_std)    
    #NOT OF DEBUG
    #'''       

    ##################################################################                                
    ######### Level3 -- Gt's children of Type in Categories ##########
    ##################################################################        
    gt_sub_subs = []
    gt_sub_subs_not_of_std = []
    if Gt_sub_sub != 'None':
        for gt in gt_subs: 
            gt_sub_subs.extend(get_gt_all_categories_children(gt))            
    gt_subs_not_of_std = get_gt_all_categories_children_not_of_std(std, gt)  #main_gts_not_of_student = all_main_gts - std_gts
   
    ##################################################################                                
    ######### Level4 -- Gt's children of Type in Categories ##########
    ##################################################################        
    gt_sub_sub_subs = []
    gt_sub_sub_subs_not_of_std = []
    if Gt_sub_sub_sub != 'None':
        for gt in gt_sub_subs: 
            gt_sub_sub_subs.extend(get_gt_all_categories_children(gt))  
    gt_sub_sub_subs_not_of_std = get_gt_all_categories_children_not_of_std(std, gt)  #main_gts_not_of_student = all_main_gts - std_gts

    #####print("gt_sub_subs", gt_sub_sub_subs)
    #####print("")
    
    whos = Accupation.query.all()
    default_who = Accupation.query.filter(Accupation.default==True).first()

    statuss = Status.query.all()
    default_status = Status.query.filter(Status.default==True).first()
        
    tags = Tag.query.all()
    default_tag = Tag.query.filter(Tag.default==True).first()
    
    std_txts = Std_general_txt.query.filter(Std_general_txt.student_id==std.id).all()

    due_date = date.today()
  
    age_ranges = Age_range.query.order_by(Age_range.title).all()
    tags = Tag.query.order_by(Tag.title).all()
    
    #'''
    print("")
    print("")
    print("IN edit_std_gts, BEFORE calling edit_all_main_gts.html --- gt_subs: ", gt_subs)
    print("")
    print("")
    #'''
    
    return render_template('./gts/table_gts/edit_all_main_gts.html', std=std,  
                                                        std_gts=std_gts, gts_not_of_student=gts_not_of_student, gt_categories=gt_categories,
                                                        gt_subs=gt_subs, gt_subs_not_of_std=gt_subs_not_of_std,
                                                        gt_sub_subs=gt_sub_subs, gt_sub_subs_not_of_std=gt_sub_subs_not_of_std,
                                                        statuss=statuss, default_status=default_status,
                                                        whos=whos, default_who=default_who,
                                                        tags=tags, age_ranges=age_ranges,
                                                        due_date=due_date)
                                                
														  		
@std.route('/edit_std_gts2/<int:selected_student_id>/<int:selected_gt_id>', methods=['GET', 'POST'])
@login_required
def edit_std_gts2(selected_student_id, selected_gt_id):

    std = student_select2(selected_student_id)
    gt = gt_select2(selected_gt_id)
      
    return edit_std_gts()


 														  		
@std.route('/get_std_gt/<int:std_id>', methods=['GET', 'POST'])
@login_required
def get_std_gt(std_id, Gt):
    
    ##print(" IN get_std_gt   std_id Gt ", std_id, Gt)
    ########import pdb; pdb.set_trace()
    
    all_std_gts = Std_general_txt.query.filter(Std_general_txt.student_id==std_id).all()
    all_type_gts = eval(Gt).query.all()
       
    for type_gt in all_type_gts:
        for std_gt in all_std_gts:
            if std_gt.general_txt in all_type_gts:
                gt = std_gt.general_txt  

    if gt != None:
        std_gt = std_general_txt_select2(std_id, gt.id)
    
    ###print("IN END OF get_std_gt")
    ###print(" std_id, Gt , std_gt, std_gt", std_id, Gt , std_gt, std_gt)
    ###print("")
    ###print("")
    ###print("")
    
    return gt
    
################ END studets gts ##################

