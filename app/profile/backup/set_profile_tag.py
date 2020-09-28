##############START set_profile_tag ###############	

@prf.route('/set_profile_tag', methods=['POST'])
@login_required
def set_profile_tag():
    
    #FROM https://stackoverflow.com/questions/43811779/use-many-submit-buttons-in-the-same-form
        
    std_txt = Std_general_txt.query.filter(Std_general_txt.selected==True).first()
       
    if std_txt == None:
        flash("Please select a student and a txt to match  first ")
        return redirect(url_for('students.edit_student_destinations'))		
    
    gt = std_txt.general_txt
    
    ''' 
    gt_tag_name = "tag"+ str(std_txt.general_txt_id)    
    gt_ar_name = "ar" + str(std_txt.general_txt_id)
    '''    
    
    gt_sts_name = "sts"+ str(std_txt.general_txt_id)
    
    gt_due_date_name = "due_date" + str(std_txt.general_txt_id)
    
    gt_who_name = "who"+ str(std_txt.general_txt_id)
           
    ##import pdb; #pdb.set_trace()

    print("")
    print("")
     
    print("")
    print("")
    

    selected_gt_status = Status.query.filter(Status.color_txt==request.form[gt_sts_name]).first()    
    if selected_gt_status != None:
        std_txt.status_id = selected_gt_status.id     
    sts = set_gt_category(gt.id, 'Status', selected_gt_status.title, 'יש לבחוק סטאטוס לטקסט')  , 
    
    if gt.type=='accupation':   # Only in case of todo there is a who button
        selected_gt_who = Accupation.query.filter(Accupation.title==request.form[gt_who_name]).first()    
        if selected_gt_who != None:
            std_txt.who_id = selected_gt_who.id     
        who = set_gt_category(gt.id, 'Accupation', selected_gt_who.title, 'יש לבחור תפקיד האחראי על המשימה')  , 
    
    gt_due_date = request.form[gt_due_date_name]                
    if gt_due_date != None:
        std_txt.due_date = gt_due_date
    #gt.due_date = gt_due_date
     
    std_txt.selected = False
        
    db.session.commit()
        
    return  redirect(url_for('students.edit_student_destinations')) 
f@prf           

##############END set_profile_tag ###############	
