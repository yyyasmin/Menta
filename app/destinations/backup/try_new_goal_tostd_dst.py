@std.route('/new_goal_to_std_dst', methods=['GET', 'POST'])
def new_goal_to_std_dst():
	
	student = Student.query.filter(Student.selected==True).first()
	if student == None:
		flash("Please select a student first ")
		return redirect(url_for('students.edit_students'))		

	destination = Destination.query.filter(Destination.selected==True).first()
	if destination == None:
		flash("Please select a destination to delete first ")
		return redirect(url_for('destinations.edit_destinations', from_dst_sort_order=0))

	if request.method == 'GET':
		return render_template('./destinations/edit_student_destinations_goals.html', student=student, destination=destination)
		   		
	goal = Goal.query.filter(Goal.selected==True).first()
	if goal == None:
		flash("Please select a goal first ")
		return redirect(url_for('select.goal_select'))		
	'''
	destination.goals.append(goal) 
	'''
	student.goals.append(goal)
	db.session.commit()  
	db.session.refresh(student)
	
	return render_template('./destinations/edit_student_destinations_goals.html', student=student, destination=destnation)
  

@std.route('/new_goal_to_std_dst2/<int:selected_student_id>/<int:selected_destination_id>', methods=['GET', 'POST'])
def new_goal_to_std_dst2(selected_student_id, selected_destination_id, selected_goal_id):
	print(selected_student_id)
	std = student_select2(selected_student_id)
	dst = destination_select2(selected_destination_id)
    
	goal = goal_select2(selected_goal_id)

	return redirect(url_for('students.destination_to_student_add'))			
