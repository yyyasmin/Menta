def update_updated_std_goal_form():

    #import pdb; pdb.set_trace()
    
    updated_std_goal = Std_goal.query.filter(Std_goal.selected==True).first()
    if updated_std_goal == None:
        flash("Please select a student's goal to update")
        return redirect(url_for('students.edit_student_goals'))

    if updated_std_goal == None:   #new Std_goal
        updated_std_goal = Std_goal(std.id, goal.id)        

    updated_std_goal.goal_title = goal.title
    updated_std_goal.goal_body = goal.body
    
    updated_std_goal.goal = goal
    updated_std_goal.student = std    
    updated_std_goal.dst_id = dst.id
    
    sts_title = request.form.get('selected_status')
    sts = Status.query.filter(Status.title==sts_title).first()
    status = Status.query.filter(Status.id==request.form['status']).first()    
    print("selected sts is status", sts, status)   
    updated_std_goal.status_id = sts.id
    updated_std_goal.status_title = sts.title
    updated_std_goal.status_color = sts.color
    
    updated_std_goal.due_date = request.form.get('due_date') 
   
    std.goals.append(updated_std_goal)			
    goal.students.append(updated_std_goal)
        
    print ("In match_goal_to_std NEW: student date  sts:",  updated_std_goal.goal, updated_std_goal.student, updated_std_goal.due_date, updated_std_goal.status_title)
    #DEBUG
    updated_std_goal = Std_goal.query.filter(Std_goal.goal_id == goal.id).filter(Std_goal.student_id==std.id).first() 	
    print("New goal is  for std is : Std_goal student is  ", updated_std_goal, std)
    goal.selected = False
    #DEBUG
    db.session.commit() 

    #print("goal_to_student_add METHOD", request.method)
    return  redirect(url_for('students.edit_student_goals')) 
        
############################################

