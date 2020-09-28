#################### create_new_dst_for_std ##################

@std.route('/create_new_dst_for_std/<int: selected_student_id>', methods=['GET', 'POST'])
def create_new_dst_for_std(selected_student_id):
    print("In destination_add")
	#import pdb; pdb.set_trace()
    
	std = Student.query.filter(Student.selected==True).first()      
	if std == None:
		flash("Please select a student first ")
		return redirect(url_for('students.edit_students'))
    print("Creating new dst for student: ", srd.first_name)

    author_id = current_user._get_current_object().id    
        
    age_ranges = Age_range.query.all()
    tags = Tag.query.all() 
    
    #########################################################################
    ### set private seurity option and disable security option selection  ###
    ### for private student which happens when                            ### 
    ### user wants to add a specific destination only to his student      ###
    #########################################################################
    
    std_age_range = get_student_default_age_range(std.birth_date)
    if request.method == 'GET':
    return render_template('create_new_dst_for_std.html', age_ranges=age_ranges,
                                              tags=tags,
                                              scrts=scrts,
                                              selected_ar_title = std_age_range, 
                                              selected_tag_title = "בחר נושא",
                                              force_selected_scrt_title = "private") 
        
    if request.form['submit'] == 'submit_age_range':
        selected_ar = set_dst_age_range()
        
        selected_ar_title = get_selected_ar_title()
        selected_tag = get_selected_tag_title()
        selected_scrt_title = get_selected_scrt_title()
            

    if request.form['submit'] == 'submit_tag':
        selected_tag = set_dst_tag()
        
        selected_ar_title = get_selected_ar_title()
        selected_tag = get_selected_tag_title()
        selected_scrt_title = get_selected_scrt_title()
           
    if request.form['submit'] == 'submit_scrt':
        selected_tag = set_dst_scrt()

        selected_ar_title = get_selected_ar_title()
        selected_tag = get_selected_tag_title()
        selected_scrt_title = get_selected_scrt_title()
    
    if  request.form['submit'] != 'submit_description':
        return render_template('add_destination.html', age_ranges=age_ranges,
                                                   tags=tags,
                                                   scrts=scrts,
                                                   selected_ar_title = selected_ar_title, 
                                                   selected_tag = selected_tag,
                                                   selected_scrt_title = selected_scrt_title)
                                                  
            
    if request.form['submit'] == 'submit_description': 
        title = request.form['title']      #Current Description  selection
        body = request.form['description']
        
        
        last_selected_ar = Age_range.query.filter(Age_range.selected == True).first()
        last_selected_tag = Tag.query.filter(Tag.selected == True).first()
        last_selected_scrt = Scrt.query.filter(Scrt.selected == True).first()
      
        new_destination = Destination(title, body, last_selected_ar.id, author_id)	
        
        new_destination.tags.append(last_selected_tag)
        new_destination.age_range_id = last_selected_ar.id
        new_destination.scret_id = last_selected_scrt.id
        
        last_selected_tag.destinations.append(new_destination)
        last_selected_ar.destinations.append(new_destination)
        last_selected_scrt.destinations.append(new_destination)
        
        #import pdb; pdb.set_trace()
        
        dummy_std = get_dummy_student()
        dummy_std.destinations.append(new_destination)

        db.session.add(new_destination)    
        db.session.commit()  
        db.session.refresh(new_destination)

        return url = redirect(url_for('students.edit_student_destinations'))
        
 #################### END create_new_dst_for_std ##################
       