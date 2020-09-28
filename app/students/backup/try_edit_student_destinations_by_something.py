
@std.route('/edit_students_destinations', methods=['GET', 'POST'])
def edit_students_destinations():
	
    std = Student.query.filter(Student.selected==True).first()
    if std == None:
        flash("Please select a student first ")
        return redirect(url_for('select.student_select'))
        
    destinations = Destination.query.filter(Destination in std.destinations).order_by(Destination.title).all() 
    age_ranges = Age_range.query.all()
    tags = Tag.query.all() 
    #import pdb; pdb.set_trace()
    default_age_range = get_student_default_age_range(std.birth_date)

    return render_template('edit_dst_in_table.html', destinations=destinations, age_ranges=age_ranges, tags=tags)															
    
    #return render_template('edit_students_destinations.html', student=student, age_ranges=age_ranges, default_age_range = default_age_range)

																												  		
@std.route('/edit_students_destinations2/edit/<int:selected_student_id>/<int:selected_destination_id>', methods=['GET', 'POST'])
def edit_students_destinations2(selected_student_id, selected_destination_id):
	print("In edit_student_destinations2 Request is :", request)
	std = student_select2(selected_student_id)
	if selected_destination_id != 0:
		dest = destination_select2(selected_destination_id)
	return redirect(url_for('students.edit_students_destinations'))		


@dst.route('/edit_student_destinations_by_age_range', methods=['GET', 'POST'])
@login_required
def edit_student_destinations_by_age_range():
    destinations = Destination.query.order_by(Destination.title).all() 
    age_ranges = Age_range.query.all()
    tags = Tag.query.all() 
    #import pdb; pdb.set_trace()
    #return render_template('edit_destinations_by_age_range.html', destinations=destinations, age_ranges=age_ranges, tags=tags )							
    return render_template('edit_dst_by_age_range.html', destinations=destinations, age_ranges=age_ranges, tags=tags)															

@dst.route('/edit_student_destinations_by_subject', methods=['GET', 'POST'])
@login_required
def edit_student_destinations_by_subject():
    destinations = Destination.query.order_by(Destination.title).all() 
    age_ranges = Age_range.query.all()
    tags = Tag.query.all() 
    #import pdb; pdb.set_trace()
    #return render_template('edit_destinations_by_subject.html', destinations=destinations, age_ranges=age_ranges, tags=tags )							
    return render_template('edit_dst_by_subject.html', destinations=destinations, age_ranges=age_ranges, tags=tags)															

@dst.route('/edit_student_destinations_by_ABC', methods=['GET', 'POST'])
@login_required
def edit_student_destinations_by_ABC():
    destinations = Destination.query.order_by(Destination.title).all() 
    age_ranges = Age_range.query.all()
    #import pdb; pdb.set_trace()
    #return render_template('edit_destinations_by_subject.html', destinations=destinations, age_ranges=age_ranges, tags=tags )							
    return render_template('edit_dst_by_ABC.html', destinations=destinations)															
