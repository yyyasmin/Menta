	
##############START TRY studets goals###############	

@std.route('/try_goal_to_student_add', methods=['GET', 'POST'])
def try_goal_to_student_add():

	print("IN goal_to_student_add")
	##################import pdb; pdb.set_trace()
	student = Student.query.filter(Student.selected==True).first()
	if student == None:
		flash("Please select a student first ")
		return redirect(url_for('goals.student_select'))

	goals_not_of_student = get_goals_not_of_student()
	#DEBUG
	print("Teachrr not in stuff list")
	for t in goals_not_of_student:
		print("t name = ", t.first_name)
	#DEBUG
	
	statuss = Status.query.filter(Status.hide == False).all()
	if request.method == 'GET':
		return render_template('./goals/edit_goals_not_of_student.html', student=student, 
																	goals_not_of_student=goals_not_of_student,
																	statuss=statuss)
																																															
	goal = Goal.query.filter(Goal.selected==True).first()
	if goal == None:
		flash("Please select a goal first ")
		return redirect(url_for('goals.goal_select'))
		
	exist_std_goal = Std_goal.query.filter(Std_goal.student_id == student.id).filter(Std_goal.goal_id==goal.id).count()
	sr = request.form.get('selected_std_goal')
	print("selected std_goal is", sr)
	
	print("exist_std_goal:", exist_std_goal)
	print("exist_std_goal:   std_goal title:", exist_std_goal, sr, request.method)
	
	if exist_std_goal == 0:   #new Std_goal
		##################import pdb; pdb.set_trace()
		std_goal = Std_goal(student.id, goal.id)
		std_goal.goal = goal
		std_goal.student = student
		student.goals.append(std_goal)			
		goal.students.append(std_goal)
		print ("Std_goal NEW title   NEW goal    NEW student  :", std_goal.title, std_goal.goal, std_goal.student)

	else:
		std_goal = Std_goal.query.filter(Std_goal.student_id == student.id).filter(Std_goal.goal_id==goal.id).first()   #update std_goal
		print("Existing Std_goal is", std_goal)
		print ("Std_goal OLD title for student and goal :", std_goal.title, std_goal.student_id, std_goal.goal_id)
		std_goal.title=sr		
		print ("Std_goal NEW title   OLD goal    OLD student  :", std_goal.title, std_goal.goal, std_goal.student)

	print("IIIIIIIIIIIIIIIIIIIIIIn updating std_goal ",  std_goal.student.id, std_goal.goal_id, std_goal.title)

	#DEBUG
	std_goal = Std_goal.query.filter(Std_goal.goal_id == goal.id).filter(Std_goal.student_id==student.id).first() 	
	print("New Reole title is: Std_goal student is   Std_goal goal is ", std_goal.title, std_goal.student, std_goal.goal)
	#DEBUG
	db.session.commit() 
	db.session.refresh(student)
	db.session.refresh(goal)
	db.session.refresh(std_goal)
	
	#print("goal_to_student_add METHOD", request.method)
	return  redirect(url_for('students.edit_student_goals')) 
		
		
	
@std.route('/try_goal_to_student_add2/<int:selected_goal_id>/<int:selected_student_id>', methods=['GET', 'POST'])
def try_goal_to_student_add2(selected_goal_id, selected_student_id):
	print(selected_student_id)
	student_select2(selected_student_id)
	#print(selected_goal_id)
	if selected_goal_id:
		goal_select2(selected_goal_id)
	return goal_to_student_add()


	
@std.route('/try_get_student_goals', methods=['GET', 'POST'])
def try_get_student_goals():
	student = Student.query.filter(Student.selected==True).first()
	if student == None:
		flash("Please select a student first ")
		return redirect(url_for('students.edit_students'))
		
	
	student_staff_goals = Goal.query.join(Std_goal).filter(Std_goal.student_id==student.id).filter(Std_goal.goal_id==Goal.id).all()

	return student_staff_goals


@std.route('/try_get_goals_not_of_student', methods=['GET', 'POST'])
def try_get_goals_not_of_student():
	student = Student.query.filter(Student.selected==True).first()
	if student == None:
		flash("Please select a student first ")
		return redirect(url_for('students.edit_students'))
	
	#DEBUG
	##################import pdb; pdb.set_trace()	
	all_goals = Goal.query.all()

	student_staff_goals = Goal.query.join(Std_goal).filter(Std_goal.student_id==student.id).filter(Std_goal.goal_id==Goal.id).all()
	
	goals_with_no_students = Goal.query.filter(~Goal.students.any()).all()
	
	goals_not_of_student = list(set(all_goals).difference(set(student_staff_goals)))  #goals_not_of_student = all_goals-student_staff_goals
	
	goals_not_of_student.extend(goals_with_no_students)

	##################import pdb; pdb.set_trace()
	#DEBUG

	return goals_not_of_student
    
############## END TRY studets goals###############	
