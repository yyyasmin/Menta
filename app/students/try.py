##############studets plan report###############
	
@std.route('/plan_report', methods=['GET', 'POST'])
def plan_report():
	
	student = Student.query.filter(Student.selected==True).first()
	if student == None:
		flash("Please select a student first ")
		return redirect(url_for('select.student_select'))
	
	student_staff_teachers = get_student_teachers()
    return render_template('plan_report.html')
    '''
	return render_template('plan_report.html',  student=student, 
                                                student_staff_teachers=student_staff_teachers,
                                                )
	'''												   		
														  		
@std.route('/plan_report2/<int:selected_student_id>, methods=['GET', 'POST'])
def plan_report2(selected_student_id, selected_teacher_id):
	print("In plan_report2 Request is :", request)
	std = student_select2(selected_student_id)

	return plan_report()
 
 	
##############studets plan report###############	
			