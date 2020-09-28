##############START update_std_gt ###############	

@std.route('/update_std_gt', methods=['POST'])
@login_required
def update_std_gt():

    author_id = current_user._get_current_object().id
    
    #FROM https://stackoverflow.com/questions/43811779/use-many-submit-buttons-in-the-same-form
        
     
    if std_gt == None:
        flash("Please select a student and a txt to match  first ")
        return redirect(url_for('students.edit_student_destinations'))		
        
    std_gt = Std_general_txt.query.filter(Std_general_txt.selected==True).first()    
    std = std_gt.student
    gt = std_t.gt
  
    txt_type = gt.gt_type
    
    print("txt_type", txt_type)
    print("")
      
    print("std_gt", std_gt)
    print("")
      
    print("std", std, std.id)
    print("")
    
    print("gt", gt, gt.id)
    print("")
    
    if txt_type == 'Destination' or txt_type == 'Goal' or txt_type == 'Todo':
        general_txt_sts_name = "sts"+ str(std_gt.general_txt_id)
        ####print( "request.form[general_txt_sts_name]", request.form[general_txt_sts_name])
        
        general_txt_date_name = "due_date" + str(std_gt.general_txt_id)
        ####print( "request.form[general_txt_date_name]", request.form[general_txt_date_name])
        
        selected_general_txt_status = Status.query.filter(Status.id==request.form[general_txt_sts_name]).first()
        if selected_general_txt_status != None:
            std_gt.status_id = selected_general_txt_status.id  
        general_txt_due_date = request.form[general_txt_date_name]                
        if general_txt_due_date != None:
            std_gt.due_date = general_txt_due_date
                    
    if txt_type == 'Todo':
        general_txt_who_name = "who"+ str(std_gt.general_txt_id)
        ####print( "request.form[general_txt_who_name]", request.form[general_txt_who_name])        
        who = Accupation.query.filter(Accupation.id==request.form.get(general_txt_who_name)).first()
        if who != None:
            std_gt.acc_id = who.id
            
    if gt.is_editable(author_id):
:
        title_name = "title" + str(gt.id)
        gt.title = request.form[title_name]                
        
        body_name = "title" + str(gt.id)
        gt.body = request.form[body_name] 

    else:
        flash("You are not authorized to change this text")
        
            
    
           
    std_gt.selected = False
        
    db.session.commit() 

    return  redirect(url_for('students.edit_student_destinations')) 


@std.route('/update_std_gt2', methods=['GET', 'POST'])
@login_required
def update_std_gt2():
    
    std = Student.query.filter(Student.selected==True).first()
    
    gt_id = int(request.form['gt.id']    # case of destination 
    print("gt", gt_id)
    import pdb; pdb.set_trace()
                
    gt = General_txt.query.filter(General_txt.id == gt_id).first()           
    std_gt = attach_gt_to_std(std.id, gt.id)
        
    std_gt = std_general_txt_select2(std.id, gt.id) 
    std_gt = General_txt_select2(std.id, gt.id)
    
    return update_std_gt()
               
\    
##############END update_std_gt ###############	
