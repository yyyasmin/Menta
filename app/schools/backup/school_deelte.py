
@scl.route('/edit_school_students', methods=['GET', 'POST'])
@login_required
def edit_school_students():

    author_id = current_user._get_current_object().id
    user = User.query.filter(User.id == author_id ).first()

    school = School.query.filter(School.selected==True).first()
    if school == None:
        flash("Please select a school first ")
        return edit_schools() 
        
    school_students = get_school_students()

    #DEBUG
    for std in school_students:
        print("student: ", std.id)
        for r in std.schools:
            print("School-Student is: student is school is role is ", r.student_id, 
                                                                      r.school_id, 
                                                                      r.title)
    #DEBUG

    return render_template('edit_school_students.html', school=school, 
                                                        is_super_user = user.is_super_user,
                                                        school_students=school_students)



@scl.route('/edit_school_students2/<int:selected_school_id>/<int:selected_student_id>', methods=['GET', 'POST'])
@login_required
def edit_school_students2(selected_school_id, selected_student_id):
	print("In edit_school_students2 Request is :", request)
	school = school_select2(selected_school_id)
	if selected_student_id != 0:
		student = student_select2(selected_student_id)
	return edit_school_students()
 
 

