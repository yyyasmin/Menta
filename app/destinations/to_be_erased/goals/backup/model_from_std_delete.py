		
@std.route('/goal_from_student_delete', methods=['GET', 'POST'])
@login_required
def std_goal_delete():

	std_goal = Std_goal.query.filter(Std_goal.selected==True).first()
	if std_goal == None:
		flash("Please select a goal first ")
		return redirect(url_for('students.edit_student_goals'))

    db.session.delete(std_goal)
    db.session.commit()

	return  redirect(url_for('students.edit_student_goals'))  #no change in students staff goals
		
@std.route('/std_goal_delete2/delete/<int:selected_std_id>/<int:selected_goal_id>', methods=['GET', 'POST'])
@login_required
def std_goal_delete2(selected_std_id, selected_goal_id):
	##print("In DDDDDDDDDDDD student_from_goal_delete2")
	std_goal = std_goal_select2(selected_std_id, selected_goal_id)
	return  redirect(url_for('students.std_goal_delete'))  
