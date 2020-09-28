	
################ START studets gts ##################
	
@std.route('/student_gts', methods=['GET', 'POST'])
@login_required
def edit_std_profile(Gt, Sub_gt1, Sub_gt2, Sub_gt3):   # for example: for student_subjects  ==> Gt = 'Subject' stored  gt.gt_type
    
    return  edit_std_main_gts('Profile', 'Subjec', 'None', 'None')
                                                    
														  		
@std.route('/edit_std_profile2/<int:selected_student_id>', methods=['GET', 'POST'])
@login_required
def edit_std_profile2(selected_student_id):

    std = student_select2(selected_student_id)
    prf = get_std_gt(std.id, 'Profile')
    if prf == None:
        print("In prf==None, BEFORE calling get_std_prf")
        prf = get_std_prf()
        print("In prf==None, AFTER calling get_std_prf")

    print("In edit_std_profile2 std std :", prf, std)

    return edit_std_profile()
  
	
@std.route('/edit_std_main_gts', methods=['GET', 'POST'])
@login_required
def edit_std_main_gts(Gt, Sub_gt1, Sub_gt2, Sub_gt3):   # for example: for student_subjects  ==> Gt = 'Subject' stored  gt.gt_type

    print(" IN student_gts Gt" , Gt )
    print("")
    
    print(" IN student_gts Sub_gt1" , Sub_gt1 )
    print("")
    
    print(" IN student_gts Sub_gt2" , Sub_gt2 )
    print("")
    
    print(" IN student_gts Sub_gt3" , Sub_gt3 )
    print("")

    import pdb; pdb.set_trace()
    
    
    std = Student.query.filter(Student.selected==True).first()
    if std == None:
        flash("Please select a student first ")
        return redirect(url_for('students.edit_students'))
  
    ############impor pdb;pdb.set_trace()
    
    std_gts = General_txt.query.join(Std_general_txt).filter(Std_general_txt.student_id==std.id).filter(Std_general_txt.general_txt_id==General_txt.id).all()
    
    ########import pdb;; pdb.set_trace()
    
    edit_std_main_gts = []    # Get all student's main gets (such as all_subjects )
    all_main_gts = eval(Gt).query.filter(eval(Gt).hide==False).all()  
    for d in all_main_gts:
        std_main_gt = Std_general_txt.query.filter(Std_general_txt.student_id==std.id).filter(Std_general_txt.general_txt_id==d.id).first()
        if std_main_gt !=None:
           edit_std_main_gts.append(d)            
    main_gts_not_of_student = list(set(all_main_gts).difference(set(edit_std_main_gts)))  #main_gts_not_of_student = all_main_gts - std_main_gts
   
    print ("edit_std_main_gts: ", edit_std_main_gts)
    print ("type: ", Gt)
    
    #####import pdb; pdb.set_trace()
    
    student_sub_gt1s = []    # Get all student' sub_gt1s
    all_sub_gt1s = eval(Sub_gt1).query.filter(eval(Sub_gt1).hide==False).all()
    ###print ("all_sub_gt1s: ", all_sub_gt1s)
    for g in std_gts:
        if g in all_sub_gt1s:
            student_sub_gt1s.append(g)
    sub_gt1s_not_of_student = list(set(all_sub_gt1s).difference(set(student_sub_gt1s)))  #sub_gt1s_not_of_student = all_destinations - std_destinations

    if Sub_gt2 != 'None':
        student_sub_gt2s = []    # Get all student' sub_gt2s
        all_sub_gt2s = eval(sub_gt2).query.filter(eval(sub_gt2).hide==False).all()
        ###print ("all_sub_gt2s: ", all_sub_gt2s)
        for g in std_gts:
            if g in all_sub_gt2s:
                student_sub_gt2s.append(g)
        sub_gt2s_not_of_student = list(set(all_sub_gt2s).difference(set(student_sub_gt2s)))  #sub_gt2s_not_of_student = all_destinations - std_destinations

    else:   # No 2nd level gts
        student_sub_gt2s = []
        all_sub_gt2s = []
        
        
    whos = Accupation.query.all()
    default_who = Accupation.query.filter(Status.body=='default').first()

    statuss = Status.query.all()
    default_status = Status.query.filter(Status.body=='default').first()
        
    tags = Tag.query.all()
    default_tag = Tag.query.filter(Tag.body=='default').first()
    
    std_txts = Std_general_txt.query.filter(Std_general_txt.student_id==std.id).all()


    due_date = date.today()

    ########import pdb;; pdb.set_trace()
    ####print("std dsts,          ", edit_std_main_gts)
    ####import pdb; pdb.set_trace()
    #print("std sub_gt1s,         ", student_sub_gt1s)
    ####print("std sub_gt2s          ", student_sub_gt2s)
    ####print("statuss        ", statuss)
    
    age_ranges = Age_range.query.order_by(Age_range.title).all()
    tags = Tag.query.order_by(Tag.title).all()


    return render_template('./gts/table_gts/edit_all_main_gts.html', std=std,  
                                                        edit_std_main_gts=edit_std_main_gts, destinations_not_of_student=destinations_not_of_student,
                                                        all_sub_gt1s=all_sub_gt1s, student_sub_gt1s=student_sub_gt1s, sub_gt1s_not_of_student=sub_gt1s_not_of_student,
                                                        all_sub_gt2s=all_sub_gt2s, student_sub_gt2s=student_sub_gt2s, sub_gt2s_not_of_student=sub_gt2s_not_of_student,
                                                        std_txts=std_txts,
                                                        statuss=statuss, default_status=default_status,
                                                        whos=whos, default_who=default_who,
                                                        tags=tags, age_ranges=age_ranges,
                                                        due_date=due_date)
                                                
														  		
@std.route('/edit_std_main_gts2/<int:selected_student_id>/<int:selected_gt_id>', methods=['GET', 'POST'])
@login_required
def edit_std_main_gts2(selected_student_id, selected_gt_id):

    std = student_select2(selected_student_id)
    gt = gt_select2(selected_gt_id)
    ########print("In edit_std_main_gts2 std std :", std, std.id)

    return edit_std_main_gts()


 														  		
@std.route('/get_std_gt/<int:std_id>', methods=['GET', 'POST'])
@login_required
def get_std_gt(std_id, Gt):

    gt = None
    std_gts = Std_general_txt.query.filter(Std_general_txt.student_id==std_id).all()
    all_type_gts = eval(Gt).query.all()
    for std_gt in std_gts:
        if std_gt.general_txt in all_type_gts:
            gt = std_gt.general_txt
    
    print("In END OF get_std_gt Gt---- eval(Gt)----- std.id----- prf---- :", Gt, eval(Gt), std.id, prf)
    print("")
    
    return gt
    
################ END studets gts ##################

 
	 