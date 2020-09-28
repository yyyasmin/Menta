	teacher = Teacher.query.filter(Teacher.selected==True).first()
	if teacher == None:
		flash("Please select a teacher first ")
		return redirect(url_for('select.teacher_select'))
	
	#DEBUG
	#import pdb; pdb.set_trace()	
	all_students = Student.query.all()
	#DEBUG
	for s in all_students:
		print("11111111111111111 Student all_students list :", s.id, s.students)
	#DEBU
	
	teacher_students_team = Student.query.join(Role).filter(Role.teacher_id==teacher.id).filter(Role.student_id==Student.id).all()
	#DEBUG
	for s in teacher_students_team:
		print("222222222222222 Student teacher_students_team list :", s.id, s.students)
	#DEBU
		
	students_with_no_teachers = Student.query.filter(~Student.teachers.any()).all()
	#DEBUG
	for s in students_with_no_teachers:
		print("3333333333333333 Student students_with_no_teachers list :", s.id, s.students)
	#DEBUG
	
	students_not_of_teachers = list(set(all_students).difference(set(teacher_students_team)))  #teachers_not_in_staff = all_teachers-student_staff_teachers
	#DEBUG
	for s in students_not_of_teachers:
		print("4444444444444444444444 Student students_not_of_teachers list :", s.id, s.students)
	#DEBUG
		
	students_not_of_teachers.extend(students_with_no_teachers)
	#DEBUG
	for s in students_not_of_teachers:
		print("5555555555555555555555 Student students_not_of_teachers list :", s.id, s.students)
	#DEBUG
		
	#import pdb; pdb.set_trace()
	#DEBUG

	return teachers_not_in_staff