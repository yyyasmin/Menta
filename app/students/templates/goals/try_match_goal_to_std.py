	
##############START match_goal_to_std ###############	

@std.route('/match_goal_to_std/<int:selected_goal_id>', methods=['POST'])
def match_goal_to_std(selected_goal_id):
    ###import pdb;pdb.set_trace()
    print("IN goal_to_student_add")
    ######################import pdb;pdb.set_trace()
    std = Student.query.filter(Student.selected==True).first()
    if std == None:
        flash("Please select a student first ")
        return redirect(url_for('destination.edit_students'))

    dst = Destination.query.filter(Destination.selected==True).first()
    if dst == None:
        flash("Please select a student first ")
        return redirect(url_for('students.edit_student_destinations'))		
   
    goal = Goal.query.filter(Goal.selected==True).first()
    if goal == None:
        flash("Please select a goal first ")
        return redirect(url_for('students.edit_student_goals'))
        
    print("IN try_goal_to_student_add2  std dst goal ", std.id, dst.id, goal.id)


    #DEBUG
    #DEBUG
    ####import pdb;pdb.set_trace()
    statuss = Status.query.all()

    exist_std_goal = Std_goal.query.filter(Std_goal.student_id == std.id).filter(Std_goal.goal_id==goal.id).count()
    sts_title = request.form.get('selected_status')
    sts = Status.query.filter(Status.title==sts_title).first() 
    print("selected sts is", sts)

    due_date = request.form.get('due_date')
    print("selected date is", due_date)

    if exist_std_goal == 0:   #new Std_goal
        ######################import pdb;pdb.set_trace()
        std_goal = Std_goal(std.id, goal.id)
        
    else:
        std_goal = Std_goal.query.filter(Std_goal.student_id == std.id).filter(Std_goal.goal_id==goal.id).first()   #update existing std_goal

    std_goal.goal = goal
    std_goal.student = std
    
    std_goal.dst_id = dst.id
   
    std_goal.status_id = sts.id
    std_goal.status_title = sts.title
    std_goal.status_color = sts.color

    std_goal.due_date = due_date

    std.goals.append(std_goal)			
    goal.students.append(std_goal)
        
    print ("Std_goal   NEW goal    NEW student  :",  std_goal.goal, std_goal.student)
    #DEBUG
    std_goal = Std_goal.query.filter(Std_goal.goal_id == goal.id).filter(Std_goal.student_id==std.id).first() 	
    print("New goal is  for std is : Std_goal student is  ", std_goal, std)
    goal.selected = False
    #DEBUG
    db.session.commit() 
    db.session.refresh(std)
    db.session.refresh(goal)
    db.session.refresh(std_goal)

    #print("goal_to_student_add METHOD", request.method)
    return  redirect(url_for('students.edit_student_goals')) 
        
		
	
@std.route('/match_goal_to_std2/<int:selected_goal_id>', methods=['GET', 'POST'])
def match_goal_to_std2(selected_goal_id):

    print("IN try_goal_to_student_add2  std dst goal ", selected_goal_id)
    import pdb;pdb.set_trace()
    
    #print(selected_goal_id)
    if selected_goal_id:
        goal_select2(selected_goal_id)
    return match_goal_to_std()
    
##############END match_goal_to_std ###############	

