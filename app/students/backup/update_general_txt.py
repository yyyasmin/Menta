  
##############START update_std_txt ###############	

@std.route('/update_std_txt', methods=['POST'])
@login_required
def update_std_txt():

    std_txt = Std_general_txt.query.filter(General_txt.selected==True).first()
    if std_txt == None:
        flash("Please select a student and a txt to match  first ")
        return redirect(url_for('students.edit_student_destinations'))		
                
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
        
    if( int(request.form['txt_type_form_button_name']) % 3 == 0 ):    # case of destination    
        selected_dst_id = request.form['goal_and_todo_form_button_name']
        selected_dst_id = int(int(selected_goal_id)/3) 
        print("IN match_txt_to_std2 -----------  selected_dst_id:  ",  selected_dst_id)
        return update_std_txt(selected_dst_id)
         
    elif( int(request.form['dst_goal_and_todo_form_button_name']) % 3 == 1 ):    # case of goal    
        selected_goal_id = request.form['txt_type_form_button_name']
        selected_goal_id = int(int(selected_goal_id)/2)   
        print("IN match_txt_to_std2 -----------  selected_goal_id:  ",  selected_goal_id)        
        return match_goal_to_std2(selected_goal_id)
        
    elif ( int(request.form['dst_goal_and_todo_form_button_name']) % 3 == 2 ):     # case of todo   
        selected_todo_id = request.form['txt_type_form_button_name']
        selected_todo_id = int((int(selected_todo_id)-1)/2)
        todo = todo_select2(selected_todo_id)
        print("IN match_txt_to_std2 -----------  selected_todo_id:  ",  selected_todo_id)        
        return match_todo_to_std2(selected_todo_id)
    
    general_txt = general_txt_select2(selected_std_id, selected_general_txt_id)
        
    return update_std_txt()
    
##############END update_std_txt ###############	


######### START  student's genearal txt #################################
