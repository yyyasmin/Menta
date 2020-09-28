
######### START  student's genearal txt #################################
  
##############START update_std_txt ###############	

@std.route('/update_std_txt', methods=['POST'])
@login_required
def update_std_txt(txt_type):
    
    #FROM https://stackoverflow.com/questions/43811779/use-many-submit-buttons-in-the-same-form
    
    std_txt = Std_general_txt.query.filter(Std_general_txt.selected==True).first()
    

    if std_txt == None:
        flash("Please select a student and a txt to match  first ")
        return redirect(url_for('students.edit_student_destinations'))		
    
    if txt_type == 'dst':
        selected_dst_status = Status.query.filter(Status.id==request.form['selected_dst_status']).first()
        if selected_dst_status != None:
            std_txt.status_id = selected_dst_status.id  
        dst_due_date = request.form['dst_due_date']
        if dst_due_date != None:
            std_txt.due_date = dst_due_date

    elif txt_type == 'goal':
        selected_goal_status = Status.query.filter(Status.id==request.form['selected_goal_status']).first()
        if selected_goal_status != None:
            std_txt.status_id = selected_goal_status.id  
        goal_due_date = request.form['goal_due_date']
        if goal_due_date != None:
            std_txt.due_date = goal_due_date

    elif txt_type == 'todo':
    
        import pdb; pdb.set_trace()
        
        todo_sts_name = "sts"+ str(std_txt.general_txt_id)
        print( "request.form[todo_sts_name]", request.form[todo_sts_name])
        
        todo_date_name = "due_date" + str(std_txt.general_txt_id)
        print( "request.form[todo_date_name]", request.form[todo_date_name])
        
        todo_who_name = "who"+ str(std_txt.general_txt_id)
        print( "request.form[todo_who_name]", request.form[todo_who_name])
        
        selected_todo_status = Status.query.filter(Status.id==request.form[todo_sts_name]).first()
        if selected_todo_status != None:
            std_txt.status_id = selected_todo_status.id  
        todo_due_date = request.form[todo_date_name]                
        if todo_due_date != None:
            std_txt.due_date = todo_due_date
        who = Accupation.query.filter(Accupation.id==request.form.get(todo_who_name)).first()
        if who != None:
            std_txt.acc_id = who.id
   
    std_txt.selected = False
        
    print("std txt: ", std_txt)
    print("std_txt.who_id", std_txt.acc_id)
    print("std_txt.status_id", std_txt.status_id)
    print("std_txt.due_date", date.today(), std_txt.due_date)
    print("std_txt.selected ", std_txt.selected)

    db.session.commit() 

    return  redirect(url_for('students.edit_student_destinations')) 


@std.route('/update_std_txt2', methods=['GET', 'POST'])
@login_required
def update_std_txt2():
    
    std = Student.query.filter(Student.selected==True).first()
        
    if( int(request.form['txt_type_form_button_name']) % 3 == 0 ):    # case of destination    
        selected_dst_id = request.form['txt_type_form_button_name']
        selected_dst_id = int(int(selected_dst_id)/3)         

        std_gt = Std_general_txt.query.filter(Std_general_txt.general_txt_id==selected_dst_id).filter(Std_general_txt.student_id==std.id).first()
        #print("BEFRE In stg_gt==none:  std_gt:  ", std_gt)
        if std_gt == None:        # create new match between std and dst
            std_gt = Std_general_txt(std.id, selected_dst_id)

            
        dst = Destination.query.filter(Destination.id == selected_dst_id).first()           
        std_gt.student = std
        std_gt.general_txt = dst
        if std_gt not in std.general_txts:   
            std.general_txts.append(std_gt)
        if std_gt not in dst.students:  
            dst.students.append(std_gt)
        db.session.commit()    
            
        std_gt = std_general_txt_select2(std.id, selected_dst_id)
                
        return update_std_txt(txt_type='dst')
         
    elif( int(request.form['txt_type_form_button_name']) % 3 == 1 ):    # case of goal    
        selected_goal_id = request.form['txt_type_form_button_name']
        selected_goal_id = int(int(selected_goal_id)/3)
        
        #print("selected_goal_id:  ", selected_goal_id)
        std_gt = Std_general_txt.query.filter(Std_general_txt.general_txt_id==selected_goal_id).filter(Std_general_txt.student_id==std.id).first()
        if std_gt == None:        # create new match between std and goal
            ##import pdb; pdb.set_trace()
            std_gt = Std_general_txt(std.id, selected_goal_id)
            
        goal = Goal.query.filter(Goal.id == selected_goal_id).first()            
        std_gt.student = std
        std_gt.general_txt = goal                
        if std_gt not in std.general_txts:
            std.general_txts.append(std_gt)
        if std_gt not in goal.students:
            goal.students.append(std_gt)
        db.session.commit()    
        
        std_gt = std_general_txt_select2(std.id, selected_goal_id) 

        return update_std_txt(txt_type='goal')
                       
    elif ( int(request.form['txt_type_form_button_name']) % 3 == 2 ):     # case of todo   
        selected_todo_id = request.form['txt_type_form_button_name']
        selected_todo_id = int((int(selected_todo_id)-1)/3)

        std_gt = Std_general_txt.query.filter(Std_general_txt.general_txt_id==selected_todo_id).filter(Std_general_txt.student_id==std.id).first()
        if std_gt == None:        # create new match between std and todo
            std_gt = Std_general_txt(std.id, selected_todo_id)
 
        todo = Todo.query.filter(Todo.id == selected_todo_id).first()    
        std_gt.student = std
        std_gt.general_txt = todo
        if std_gt not in std.general_txts:
            std.general_txts.append(std_gt)
        if std_gt not in todo.students:
            todo.students.append(std_gt)
        db.session.commit()    
               
        std_gt = std_general_txt_select2(std.id, selected_todo_id) 
                
        return update_std_txt(txt_type='todo')
             
      
    return update_std_txt()
    
##############END update_std_txt ###############	


######### START  student's genearal txt #################################
