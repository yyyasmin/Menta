######### START  std genearal txt #################################

  
##############START match_general_txt_to_std ###############	

@std.route('/update_std_txt', methods=['POST'])
@login_required
def update_std_txt():

    ####################import pdb;;;;;pdb.set_trace()
    #print("IN general_txt_to_student_add")
    ###########################impor pdb;pdb.set_trace()
    

    std_txt = Std_general_txt.query.filter(General_txt.selected==True).first()
    if std_txt == None:
        flash("Please select a student and a txt to match  first ")
        return redirect(url_for('students.edit_student_destinations'))		
             
   
    statuss = Status.query.all()


    ########import_pdb;pdb.set_trace()
    
    sts_title = request.form.get('selected_status')
    sts = Status.query.filter(Status.title==sts_title).first() 
    std_txt.status_id = sts.id
    #print("selected sts is  sts-color ts-title: ", sts, sts.color, sts.title)   
    
    std_txt.due_date = request.form.get('due_date') 
    
    std_txt.selected = False
    db.session.commit() 

    return  redirect(url_for('students.edit_student_destinations')) 
        
		
	
@std.route('/update_std_txt2/<int:selected_std_id><int:selected_general_txt_id>', methods=['GET', 'POST'])
@login_required
def update_std_txt2(selected_std_id, selected_general_txt_id):

    print("IN match_general_txt_to_std2   general_txt ", selected_general_txt_id)
    
    ###import_pdb; pdb.set_trace()
    general_txt = general_txt_select2(selected_std_id, selected_general_txt_id)
        
    return update_std_txt()
    
##############END match_general_txt_to_std ###############	


######### START  std genearal txt #################################
