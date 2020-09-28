	
##############START studets goals###############	
	
@std.route('/edit_student_goals', methods=['GET', 'POST'])
def edit_student_goals():
	
	student = Student.query.filter(Student.selected==True).first()
	if student == None:
		flash("Please select a student first ")
		return redirect(url_for('students.edit_students'))
	
	student_goals = get_student_goals()
	return render_template('./goals/edit_student_goals.html', student=student, 
														      student_goals=student_goals
														   		
														  		
@std.route('/edit_student_goals2/<int:selected_student_id>/<int:selected_goal_id>', methods=['GET', 'POST'])
def edit_student_goals2(selected_student_id, selected_goal_id):
	print("In edit_student_goals2 Request is :", request)
	std = student_select2(selected_student_id)
	if selected_goal_id != 0:
		tchr = goal_select2(selected_goal_id)
	return edit_student_goals()
 
 
@std.route('/goal_to_student_add', methods=['GET', 'POST'])
def goal_to_student_add():


    std = Student.query.filter(Student.selected==True).first()
    if std == None:
        flash("Please select a student first ")
        return redirect(url_for('students.edit_students'))		

    goal = Goal.query.filter(Goal.selected==True).first()
    if goal == None:
        flash("Please select a goal first ")
        return redirect(url_for('goals.edit_student_goals'))

    print("IN goal_to_student_add std goal", std, goal)
    
    ################import pdb; pdb.set_trace()
    
    if request.method == 'GET':
        goals_not_of_student = get_goals_not_of_student()
        return render_template('./destinations/edit_goals_not_of_student.html', std=std, goal=goal, goals=goals_not_of_student)
 
    print("&&&&&&&&&& In goal_to_student_add std dst goal : ", std, dst, goal )

	std_goal = Std_goal.query.filter(Std_goal.student_id == student.id).filter(Std_goal.goal_id==goal.id).count()
	
	print("std_goal:", std_goal)
	print("std_goal:   goal title:", std_goal, sg, request.method)
	
	if std_goal == None:   #This goal doe'nt exist in database
        flash("Please select a goal first ")
        return redirect(url_for('goals.edit_student_goals'))

    print ("IN goal_to_student_add Std_goal : title  student  goal :", std_goal.title, std_goal.student_id, std_goal.goal_id)

    std_goal.goal_id =    goal.id
    std_goal.student_id = std.id
    std_goal.dst_id =     dst.id
    std_goal.due_date = request.form.get('due_date')
    status = request.form.get('selected_status')
    std_goal.status_id = status.id
 
    db.session.commit()  
    db.session.refresh(std)    
    return redirect(url_for('students.edit_student_destinations_goals', from_dst_sort_order=0))


    std_goal.goal = goal
    std_goal.student = student
    student.goals.append(std_goal)			
    goal.students.append(std_goal)
    
    goal.selected = False;

        
    print ("Std_goal NEW title   NEW goal    NEW student  :", std_goal.title, std_goal.goal, std_goal.student)

	print("IIIIIIIIIIIIIIIIIIIIIIn updating std_goal ",  std_goal.student.id, std_goal.goal_id, std_goal.title)

	#DEBUG
	std_goal = Std_goal.query.filter(Std_goal.goal_id == goal.id).filter(Std_goal.student_id==student.id).first() 	
	print("New Reole title is: Std_goal.title Std_goal.student is   Std_goal.goal is ", std_goal.title, std_goal.student, std_goal.goal)
	#DEBUG
    
	db.session.commit()
    
	db.session.refresh(goal)
	db.session.refresh(std_goal)
	
	return  redirect(url_for('students.edit_student_goals')) 
		
		
	
@std.route('/goal_to_student_add2/<int:selected_goal_id>/<int:selected_student_id>', methods=['GET', 'POST'])
def goal_to_student_add2(selected_goal_id, selected_student_id):
	print(selected_student_id)
	student_select2(selected_student_id)
	#print(selected_goal_id)
	if selected_goal_id:
		goal_select2(selected_goal_id)
	return goal_to_student_add()

		
@std.route('/goal_from_student_delete', methods=['GET', 'POST'])
def goal_from_student_delete():
	###############import pdb; pdb.set_trace()
	student = Student.query.filter(Student.selected==True).first()
	if student == None:
		flash("Please select a student first ")
		return redirect(url_for('students.edit_students'))

	goal = Goal.query.filter(Goal.selected==True).first()
	if goal == None:
		flash("Please select a goal first ")
		return redirect(url_for('select.goal_select'))
		
	#print("SSSSSRRRRR IN student_from_goal_delete   deleteing student %s from goal %s :",student.id, goal.id )			
	std_goal = Std_goal.query.filter(Std_goal.student_id == student.id).filter(Std_goal.goal_id==goal.id).first()   #update std_goal
	if std_goal:	
		###############import pdb; pdb.set_trace()
		print ("deleting  ROLE  ", std_goal.title)
		db.session.delete(std_goal)
		db.session.commit()
	
	return  redirect(url_for('students.edit_student_goals'))  #no change in students staff goals
		
@std.route('/goal_from_student_delete2/delete/<int:selected_goal_id>/<int:selected_student_id>', methods=['GET', 'POST'])
def goal_from_student_delete2(selected_goal_id, selected_student_id):
	#print("In DDDDDDDDDDDD student_from_goal_delete2")
	std = student_select2(selected_student_id)
	if selected_goal_id:
		#print(selected_goal_id)
		tchr = goal_select2(selected_goal_id)
	return  redirect(url_for('students.goal_from_student_delete'))  

	
	
@std.route('/get_student_goals', methods=['GET', 'POST'])
def get_student_goals():
	student = Student.query.filter(Student.selected==True).first()
	if student == None:
		flash("Please select a student first ")
		return redirect(url_for('students.edit_students'))
			
	student_goals = Goal.query.join(Std_goal).filter(Std_goal.student_id==student.id).filter(Std_goal.goal_id==Goal.id).all()

	return student_goals


@std.route('/get_goals_not_of_student', methods=['GET', 'POST'])
def get_goals_not_of_student():
	student = Student.query.filter(Student.selected==True).first()
	if student == None:
		flash("Please select a student first ")
		return redirect(url_for('students.edit_students'))
	
	###############import pdb; pdb.set_trace()	
	all_goals = Goal.query.all()


	student_goals = Goal.query.join(Std_goal).filter(Std_goal.student_id==student.id).filter(Std_goal.goal_id==Goal.id).all()
	
	goals_with_no_students = Goal.query.filter(~Goal.students.any()).all()
	
	goals_not_of_student = list(set(all_goals).difference(set(student_goals)))  #goals_not_in_staff = all_goals-student_staff_goals
	
	goals_not_of_student.extend(goals_with_no_students)

	###############import pdb; pdb.set_trace()

	return goals_not_in_staff

##############studets goals###############	
